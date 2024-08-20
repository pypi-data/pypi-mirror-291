#
# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
"""API interface for Collections."""
import asyncio
import logging
import sys
from typing import Optional

from ngcbpc.api.configuration import Configuration
from ngcbpc.api.pagination import pagination_helper
from ngcbpc.constants import CANARY_ENV, PRODUCTION_ENV, STAGING_ENV
from ngcbpc.data.model.RequestStatus import RequestStatus
from ngcbpc.errors import NgcAPIError
from ngcbpc.transfer import utils as xfer_utils
from ngcbpc.util.utils import extra_args
from registry.api.utils import (
    create_publish_artifact,
    get_environ_tag,
    SimpleRegistryTarget,
)
from registry.constants import CollectionArtifacts
from registry.data.publishing.PublishingRequest import PublishingRequest
from registry.printer.collection import CollectionPrinter

environ_tag = get_environ_tag()
env = {PRODUCTION_ENV: "prod", CANARY_ENV: "canary", STAGING_ENV: "stg"}.get(environ_tag)
ENDPOINT_VERSION = "v2"

logger = logging.getLogger(__name__)


class CollectionAPI:  # noqa: D101
    def __init__(self, connection, api_client=None):
        self.connection = connection
        self.api_client = api_client
        self.resource_type = "COLLECTIONS"
        self.printer = CollectionPrinter()
        self.config = Configuration()

    @staticmethod
    def _get_guest_base_endpoint():
        """Build out the base collection endpoint which can be extended to all possible endpoints (/v2/collections)."""
        return [ENDPOINT_VERSION, "collections"]

    def _get_guest_endpoint(self, org, team=None):
        """Interpolate org and team parameters onto guest endpoint in the form `/v2/collections/{org}[/team]`."""
        endpoint = self._get_guest_base_endpoint()
        endpoint.append(org)
        if team:
            endpoint.append(team)
        return endpoint

    @staticmethod
    def _get_auth_endpoint(org, team=None):
        """Build base auth endpoint which requires org in all cases, unlike the guest endpoint.  Construct in the form
        /v2/org/{org}/[team/{team}/]collections
        """  # noqa: D205, D415
        endpoint = [ENDPOINT_VERSION, "org", org]
        if team:
            endpoint.extend(["team", team])
        endpoint.append("collections")
        return endpoint

    @staticmethod
    def _get_find_endpoint(org, artifact_type, artifact_name, team=None, has_key=False):
        """Build the find endpoint which takes on a different form than the rest of the ones in the collections
        controller.  The authenticated endpoint is in the form
            /v2/org/{org}/[team/{team}/]{artifact_type}/{artifact_name}/collections
        The guest endpoints is in the form
            /v2/{artifact_type}/org/{org}/team/{team}/{artifact_name}/collections
        """  # noqa: D205, D415
        endpoint = [ENDPOINT_VERSION]
        org_team = ["org", org]
        if team:
            org_team.append("team")
            org_team.append(team)

        if has_key:
            endpoint.extend(org_team)
            endpoint.append(artifact_type)
        else:
            endpoint.append(artifact_type)
            endpoint.extend(org_team)

        endpoint.append(artifact_name)
        endpoint.append("collections")

        return endpoint

    def create_collection(self, collection_request, org, team=None):  # noqa: D102
        endpoint = "/".join(self._get_auth_endpoint(org, team=team))

        collection_response = self.connection.make_api_request(
            "POST",
            endpoint,
            payload=collection_request.toJSON(),
            auth_org=org,
            auth_team=team,
            operation_name="post collection",
        )

        return collection_response

    def patch_collection(self, collection_name, collection_update, org, team=None):  # noqa: D102
        endpoint = self._get_auth_endpoint(org, team=team)
        endpoint.append(collection_name)
        endpoint = "/".join(endpoint)

        collection_response = self.connection.make_api_request(
            "PATCH",
            endpoint,
            payload=collection_update.toJSON(),
            auth_org=org,
            auth_team=team,
            operation_name="patch collection",
        )
        return collection_response

    @staticmethod
    def _flatten_request_items(request_dict):
        flat = []
        for key, requests in request_dict.items():
            flat.extend([(key, itm) for itm in requests])
        return flat

    def make_artifacts_requests(self, request_dict, org, collection_name, team=None, verb="PUT"):  # noqa: D102
        endpoint = "/".join(self._get_auth_endpoint(org, team=team))
        if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith("win"):
            # Windows has been unable to close the asyncio loop successfully. This line of code is a fix
            # to handle the asyncio loop failures. Without it, code is unable to CTRL-C or finish.
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        return asyncio.run(self._make_artifacts_requests(endpoint, request_dict, org, collection_name, team, verb))

    async def _make_artifacts_requests(self, endpoint, request_dict, org, collection_name, team, verb):
        response_dict = {key: [] for key in request_dict}
        error_dict = {key: [] for key in request_dict}
        request_items = self._flatten_request_items(request_dict)
        results = await xfer_utils.gather(
            [
                self._artifact_request(collection_name, verb, endpoint, key, request, org, team)
                for key, request in request_items
            ],
        )
        for success, fail in results:
            for key, val in success.items():
                response_dict[key].append(val)
            for key, val in fail.items():
                error_dict[key].append(val)
        return response_dict, error_dict

    async def _artifact_request(self, collection_name, verb, endpoint, key, request, org, team):
        succeed = {}
        fail = {}
        artifact_org, artifact_team, artifact_name, api_target = request
        org_team = ["org", artifact_org]
        if artifact_team:
            org_team.append("team")
            org_team.append(artifact_team)
        org_team = "/".join(org_team)
        artifact_target = [artifact_org]
        if artifact_team:
            artifact_target.append(artifact_team)
        artifact_target.append(artifact_name)
        artifact_target = "/".join(artifact_target)
        try:
            response = await self.connection.make_async_api_request(
                verb,
                f"{endpoint}/{collection_name}/artifacts/{org_team}/{api_target}/{artifact_name}",
                auth_org=org,
                auth_team=team,
                operation_name="put collection artifact",
            )
            response = RequestStatus(response["requestStatus"])
            succeed[key] = (artifact_target, response)
        except NgcAPIError as e:
            request_status = e.explanation["requestStatus"]
            response = RequestStatus(request_status)
            fail[key] = (artifact_target, response)
        return succeed, fail

    def list_collections(self, org=None, team=None):  # noqa: D102
        endpoint = self._get_guest_base_endpoint()
        if org:
            endpoint = self._get_auth_endpoint(org, team=team)

        endpoint = "/".join(endpoint) + "?"  # Hack to mark the end of the API and start of params from pagination
        for page in pagination_helper(
            self.connection, endpoint, org_name=org, team_name=team, operation_name="get collection list"
        ):
            yield page

    def get_info(self, org, team, name, has_key=False):  # noqa: D102
        urls = []
        base = []
        if has_key:
            base = self._get_auth_endpoint(org, team)
        else:
            base = self._get_guest_endpoint(org, team)
        base.append(name)

        urls.append("/".join(base))
        for artifact in CollectionArtifacts:
            base = urls[0]
            urls.append(base + f"/artifacts/{artifact.value}")

        # Parameterize URL encodings
        params = [None] * len(urls)
        params[0] = {"resolve-labels": "false"}

        resp = self.connection.make_multiple_request(
            "GET", urls, params=params, auth_org=org, auth_team=team, operation_name="get collection"
        )

        return resp

    def remove(self, org, name, team=None):  # noqa: D102
        endpoint = self._get_auth_endpoint(org, team=team)
        endpoint.append(name)
        endpoint = "/".join(endpoint)
        return self.connection.make_api_request(
            "DELETE", endpoint, auth_org=org, auth_team=team, operation_name="delete collection"
        )

    def find(self, org, artifact_type, artifact_name, team=None, has_key=False):
        """Get list of collections containing a an artifact."""
        endpoint = self._get_find_endpoint(org, artifact_type, artifact_name, team=team, has_key=has_key)

        endpoint = "/".join(endpoint) + "?"  # Hack to mark the end of the API and start of params from pagination
        for page in pagination_helper(
            self.connection, endpoint, org_name=org, team_name=team, operation_name="get artifact collection list"
        ):
            yield page

    @extra_args
    def publish(
        self,
        target,
        source: Optional[str] = None,
        metadata_only=False,
        visibility_only=False,
        allow_guest: Optional[bool] = False,
        discoverable: Optional[bool] = False,
        public: Optional[bool] = False,
    ):
        """Publishes a collection with options for metadata, and visibility.

        This method manages the publication of a collection of artifacts, handling
        different aspects of the publication such as metadata only, and
        visibility adjustments. It validates the combination of arguments provided
        and processes the publication accordingly.
        """  # noqa: D401
        self.api_client.registry.publish.validate_args(
            target,
            source,
            metadata_only,
            False,
            visibility_only,
            allow_guest,
            discoverable,
            public,
        )

        if metadata_only:
            self.copy_metadata(target, source)
        elif visibility_only:
            self.update_visibility(target, allow_guest, discoverable, public)
        else:
            self.copy_metadata(target, source)
            self.update_visibility(target, allow_guest, discoverable, public)
        logger.debug("Successfully published %s", target)

    def copy_metadata(self, target, source) -> None:  # noqa: D102
        self.config.validate_configuration(guest_mode_allowed=False)
        _source = SimpleRegistryTarget(source, org_required=True, name_required=True)
        _target = SimpleRegistryTarget(target, org_required=True, name_required=True)
        request = PublishingRequest()
        request.artifactType = "COLLECTION"
        request.sourceArtifact = create_publish_artifact(_source.org, _source.team, _source.name)
        request.targetArtifact = create_publish_artifact(_target.org, _target.team, _target.name)

        return self.api_client.registry.publish.copy_metadata_artifact(
            request, self.resource_type, self.config.org_name, self.config.team_name
        )

    def update_visibility(self, target, allow_guest, discoverable, public) -> None:  # noqa: D102
        self.config.validate_configuration(guest_mode_allowed=False)
        _target = SimpleRegistryTarget(target, org_required=True, name_required=True)
        request = PublishingRequest()
        request.artifactType = "COLLECTION"
        request.targetArtifact = create_publish_artifact(_target.org, _target.team, _target.name)

        request.publishToPublic = public
        request.publishWithGuestAccess = allow_guest
        request.publishAsListedToPublic = discoverable

        return self.api_client.registry.publish.update_visibility(
            request, self.resource_type, self.config.org_name, self.config.team_name
        )
