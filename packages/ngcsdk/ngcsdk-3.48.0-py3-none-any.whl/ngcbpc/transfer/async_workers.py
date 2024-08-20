#
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
from abc import ABC, abstractmethod
import asyncio
import base64
from concurrent.futures import ProcessPoolExecutor
import json
import os
import signal
import time
from typing import (
    Any,
    AsyncGenerator,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)

import aiofiles
import aiohttp
from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
from opentelemetry.instrumentation.asyncio import AsyncioInstrumentor

from ngcbpc.api.authentication import Authentication
from ngcbpc.api.utils import add_scheme
from ngcbpc.environ import (
    NGC_CLI_API_URL,
    NGC_CLI_PROGRESS_UPDATE_FREQUENCY,
    NGC_CLI_TRANSFER_CHUNK_SIZE,
    NGC_CLI_UPLOAD_RETRIES,
)
from ngcbpc.errors import NgcException
from ngcbpc.transfer.utils import (
    async_retry,
    bitmask_clear_bit,
    bitmask_get_set_bits,
    bitmask_is_bit_set,
    bitmask_set_bit_in_size,
    get_sha256_file_checksum,
    log_debug,
)

TRANSFER_CONNECTION_TIMEOUT = 300

# contractral constant, cannot be modified without agreement
PARTITION_SIZE = 500000000

# This line instruments aiohttp client sessions and requests, enabling tracing functionality.
# It adds default trace configuration options to all aiohttp requests
AioHttpClientInstrumentor().instrument()

# This line instruments all asyncio functions, enabling tracing without the need to pass a tracer explicitly.
# In asyncio workers, where different contexts may exist for the overall execution and individual worker tasks,
# this instrumentation ensures that tracing captures and respects the distinct contexts of each worker's execution.
AsyncioInstrumentor().instrument()

NodeT = TypeVar("NodeT", bound="BaseFileNode")


class AsyncTransferProgress:
    """Tracks the state of a file during async transfer.

    Track overall transfer progress for a transfer, providing safe async updates and callback
    at a specified maximum update rate.
    """

    def __init__(
        self,
        completed_bytes: int = 0,
        failed_bytes: int = 0,
        total_bytes: int = 0,
        completed_count: int = 0,
        failed_count: int = 0,
        total_count: int = 0,
        callback_func: Optional[  # pylint: disable=unsubscriptable-object
            Callable[[int, int, int, int, int, int], Any]
        ] = None,
        update_rate=NGC_CLI_PROGRESS_UPDATE_FREQUENCY,
    ):
        """Initialize the AsyncTransferProgress instance.

        Args:
            completed_bytes (int): The number of completed bytes.
            failed_bytes (int): The number of failed bytes.
            total_bytes (int): The total number of bytes.
            completed_count (int): The number of completed items.
            failed_count (int): The number of failed items.
            total_count (int): The total number of items.
            callback_func (Optional[Callable[[int, int, int, int, int, int], Any]]):
                A callback function that accepts six integers representing
                completed_bytes, failed_bytes, total_bytes, completed_count,
                failed_count, and total_count respectively. If provided,
                this function will be called to report progress.
                If set to None, progress updates will not be reported.
            update_rate (float): The maximum update rate for the callback function,
                in seconds. Progress updates will be reported at most once per
                this duration. Ignored if callback_func is None.

        """
        self.lock = asyncio.Lock()
        self.completed_bytes = completed_bytes
        self.failed_bytes = failed_bytes
        self.total_bytes = total_bytes
        self.completed_count = completed_count
        self.failed_count = failed_count
        self.total_count = total_count
        self.callback_func = callback_func

        self.update_rate = update_rate if callback_func else -1
        self.next_update = time.time() + update_rate if callback_func else -1

    async def debounced_update_progress(self):
        """Call the update progress callback function if the specified update rate interval has passed.

        'callback_func' is a user provided function with limited capability during lots of concurrent updates.
        Be sure to call update_progress at the end to finalize progress update.
        """
        now = time.time()  # tiny bit less expensive than lock check, thus do it first
        if self.callback_func and now > self.next_update and (not self.lock.locked()):
            async with self.lock:
                self.next_update = now + self.update_rate
                self.update_progress()

    def update_progress(self):
        """Call the update progress callback function with the current progress metrics."""
        if self.callback_func:
            self.callback_func(
                self.completed_bytes,
                self.failed_bytes,
                self.total_bytes,
                self.completed_count,
                self.failed_count,
                self.total_count,
            )

    async def advance(self, size_in_bytes: int, count: int):
        """Advance the progress by adding completed bytes and item count.

        use negatives to undo
        """
        async with self.lock:
            self.completed_bytes += size_in_bytes
            self.completed_count += count
        await self.debounced_update_progress()

    async def fail(self, size_in_bytes: int, count: int):
        """Update the progress by adding failed bytes and item count.

        use negatives to undo
        """
        async with self.lock:
            self.failed_bytes += size_in_bytes
            self.failed_count += count
        await self.debounced_update_progress()

    def read_progress(self):
        """Read the current progress metrics."""
        return (
            self.completed_bytes,
            self.failed_bytes,
            self.total_bytes,
            self.completed_count,
            self.failed_count,
            self.total_count,
        )


class BaseFileNode:  # noqa: D101
    def __init__(
        self,
        file_path: str = "",
        size: int = -1,
        ftime: float = -1.0,
        bitmask: int = -1,
    ):
        """This base file node object tracks the state of a file during transfer.

        FileNode-level asynchronous access should be handled in child classes.
        Read operations typically do not require locking, while write operations usually do.
        Users can implement their own logic for bitmask manipulation if needed.

        Args:
            file_path (str): The path to the file being tracked.
            size (int): The size of the file in bytes.
            ftime (float): A time of the file (Unix timestamp) to record for syncing.
            bitmask (int): The progress bitmask, default intepretation:
                           - 1 represents incomplete status,
                           - 0 represents complete status,
                           - A bitmask value of 0 indicates that all partitions are completed.
        """  # noqa: D401, D404
        self.lock = asyncio.Lock()

        # file metadata
        self.file_path = file_path
        self.size = size
        self.ftime = ftime

        # progress states
        self.bitmask = bitmask

        # temporay states
        # write_change is for AOF persistence
        # are there changes since load | should we persist this node
        self.write_change = False
        # has this file node caused a failure already
        self.failed = False

    @abstractmethod
    def serialize(self) -> str:
        """Serialize the instance state to a string for persistence. concrete method should choose what to persist."""

    @abstractmethod
    def is_match(self) -> bool:
        """Set condition for the instance matches the system file to ensure it is the same file."""

    @abstractmethod
    def is_sync(self) -> bool:
        """Set condition for the instance matches the system file and it is synced(same file and done)."""

    @classmethod
    def deserialize(cls, state: str):
        """Deserialize a JSON string to a file node.

        This method loads the state of the file node from a JSON string.
        """
        data = json.loads(state)
        ins = cls()
        for key, val in data.items():
            setattr(ins, key, val)
        return ins

    def is_partition_complete(self, partition_id: int) -> bool:
        """Check if a partition is completed."""
        return not bitmask_is_bit_set(self.bitmask, partition_id)

    def get_completed_size(self) -> int:
        """Provide the sum of completed partition sizes in bytes."""
        return self.size - bitmask_set_bit_in_size(self.bitmask, self.size, PARTITION_SIZE)

    async def set_partition_complete(self, partition_id: int):
        """Mark one partition complete."""
        async with self.lock:
            self.bitmask = bitmask_clear_bit(self.bitmask, partition_id)
            self.write_change = True


class UploadFileNode(BaseFileNode):  # noqa: D101
    def __init__(
        self,
        file_path: str = "",
        size: int = -1,
        ftime: float = -1.0,
        bitmask: int = -1,
        upload_id="",
        hash="",
        race_flag=False,
        complete=False,
    ):
        """Initialize the upload file node with additional attributes for upload management.

        This class extends BaseFileNode to include attributes specific to upload management.

        Attributes:
            upload_id (str): Identifier set after initiating a multipart upload.
            hash (str): Hash computed by the worker for the file.
            race_flag (bool): Flag necessary to prevent racing condition when multiple producers
                              send the same workload to the consumer. Only one should succeed.
            complete (bool): Marked complete state unique to multipart upload.
        """
        super().__init__(file_path=file_path, size=size, ftime=ftime, bitmask=bitmask)
        self.upload_id = upload_id
        self.hash = hash
        self.race_flag = race_flag
        self.complete = complete

    def serialize(self):
        """Convert the upload file node state to a string.

        This method converts the upload filenode states to a JSON string representation.
        Unnecessary fields are removed to conserve space in serialization.
        """
        include_fields = ["size", "ftime", "bitmask", "upload_id", "hash", "complete", "file_path"]
        state = {field: getattr(self, field) for field in include_fields}
        return json.dumps(state)

    def is_match(self) -> bool:
        """Check if the instance matches the system file to ensure it is still the same file."""
        # this is the same aws upload sync strategy
        # https://github.com/aws/aws-cli/blob/master/awscli/customizations/s3/syncstrategy/base.py#L226
        return (
            os.path.isfile(self.file_path)
            and self.size == os.path.getsize(self.file_path)
            and self.ftime == os.path.getmtime(self.file_path)
        )

    def is_sync(self) -> bool:
        """Check if the instance still matches the system file and synced with remote."""
        return self.is_match() and self.complete

    async def set_file_hash(self, hash):
        """Set the hash for the file."""
        async with self.lock:
            self.hash = hash
            self.write_change = True

    async def set_complete(self):
        """Mark the file as complete."""
        async with self.lock:
            self.complete = True
            self.write_change = True

    async def set_race_flag_once(self) -> bool:
        """Determine whether the file should be send to mark completion.

        This method determines whether the file should be send to the consumer
        for further processing. It requires a lock since multiple producers may
        concurrently attempt to send the same workload to the consumer, and the
        consumer take time to perform mark completion.

        Returns:
            bool: True if the file is not yet send to the consumer and additional action is needed,
            False if the file is already or will be send to the consumer no additional action is needed.
        """
        async with self.lock:
            should_mark_complete = bool(
                (self.bitmask == 0)  # All partitions uploaded
                and self.hash  # Hashing completed
                and (not self.complete)  # Not already marked as complete
                and (not self.race_flag)  # No other worker marking completion
            )
            if should_mark_complete:
                # Block further attempts to mark as complete
                self.race_flag = True
            return should_mark_complete

    async def set_failed_once(self) -> bool:
        """Determine whether the file should be marked as failed.

        This method determines whether the file should be marked as failed and
        further processing. It requires a lock since multiple consumers may concurrently
        attempt to fail the same file, but only one consumer should mark it as failed.

        Returns:
            bool: True if the file is marked as failed and additional action is needed,
            False if the file is already marked as failed and no additional action is needed.
        """
        async with self.lock:
            if self.failed:
                # If already marked as failed, no additional action needed
                return False
            # Mark the file as failed and perform additional action
            self.failed = True
            return True


class DownloadFileNode(BaseFileNode):
    """Placeholder class for extending type hinting and code structure.

    This class serves as a placeholder for extending type hinting and code structure.
    It will be further developed in the future.
    """

    def __init__(self):
        """Initialize the download file node."""
        raise NotImplementedError()

    def serialize(self):
        """Convert the download file node state to a string."""
        raise NotImplementedError()

    def is_match(self) -> bool:
        """Check if the instance matches the system file to ensure it is still the same file."""
        raise NotImplementedError()

    def is_sync(self) -> bool:
        """Check if the instance still matches the system file and synced with remote."""
        raise NotImplementedError()


class BaseCompletionTable(Generic[NodeT], ABC):
    """A base class for managing a completion table for file nodes during file transfer.

    The Completion table manages file nodes using a dictionary (absolute_file_path: file_node),
    tracks their state during file transfer, and provides high-level operations for managing
    file nodes, such as creating, deleting, and checking the status of file nodes.
    """

    def __init__(self, table_file_path=None):
        """Initialize the base completion table.

        Args:
            table_file_path (Optional[str]): The file path to store the table data.

        """
        self.table: Dict[str, NodeT] = {}
        self.table_file_path = table_file_path

    # High level managed file node operations
    @abstractmethod
    def create_file_node(self, file_path: str) -> NodeT:
        """Create a file node for the type of completion table.

        This method should be implemented in child classes to create a specific
        type of file node (e.g., upload or download) based on the transfer type.
        """

    def is_file_match(self, file_path: str) -> bool:
        """Check if the file path is matched with an existing file node."""
        return file_path in self.table and self.table[file_path].is_match()

    def is_file_sync(self, file_path: str) -> bool:
        """Check if the file path is synchronized with an existing file node."""
        return file_path in self.table and self.table[file_path].is_sync()

    def get_file_node(self, file_path: str) -> Union[NodeT, None]:
        """Retrieve the file node for the given file path."""
        return self.table.get(file_path, None)

    def calculate_checked_file_completion(self, file_path: str) -> Tuple[int, int]:
        """Calculate the completion status of a file with integrity check.

        This method calculates the completion status of a file by retrieving the
        file node, checking if it matches the actual file, and then return the
        completed size and completed count.
        """
        fn = self.get_file_node(file_path)
        if fn is None:
            return 0, 0
        if not fn.is_match():
            return 0, 0
        return fn.get_completed_size(), fn.is_sync() * 1

    def get_checked_file_node(self, file_path: str) -> Union[NodeT, None]:
        """Retrieve a checked file node for the given file path with integrity check.

        If the file is synced, it deletes the file node entry from table and return None.
        If the file matches but not synced, it returns the file node.
        If the file does not match or not in table, it creates and returns a new file node.
        """
        if self.is_file_match(file_path):  # filenode matches os file
            if self.is_file_sync(file_path):  # filenode synced, transfer complete
                self.delete_file_node(file_path)  # clear this entry
                return None  # transfer complete, nothing to do
            return self.get_file_node(file_path)  # return this filenode
        return self.create_file_node(file_path)  # get a new file node

    def delete_file_node(self, file_path: str):
        """Delete the file node for the given file path from the table."""
        if file_path in self.table:
            self.table.pop(file_path)

    def save_all_file_nodes(self):
        """Save all file nodes in the table to the `table_file_path` file.

        This method saves the state of all file nodes in the table to file.
        It skips nodes that do not need to write changes.

        This method is typically used during emergency stops to ensure the state
        of the table is preserved.
        """
        if self.table_file_path is None:
            return
        with open(self.table_file_path, "a") as f:
            for _, fn in self.table.items():
                if fn.write_change:
                    f.write(fn.serialize() + "\n")
            # no cleanup, this is probably an emergency stop

    async def async_save_file_node(self, file_path: str):
        """Asynchronously save a specific file node to the `table_file_path` file.

        This method saves the state of a specific file node to file asynchronously.
        It skips nodes that do not have write changes and deletes the file node after a successful write.
        This is typically used in async loop to incrementally write completed file nodes to file,
        so table size is bound.
        """
        if self.table_file_path is None:
            return
        fn = self.get_file_node(file_path)
        if fn is not None and fn.write_change:
            async with aiofiles.open(self.table_file_path, "a") as f:
                await f.write(fn.serialize() + "\n")

            # cleanup on successful write,
            # still in async loop
            self.delete_file_node(file_path)

    def is_table_file_exist(self) -> bool:
        """Check if the `table_file_path` file exists."""
        if self.table_file_path is None:
            return False
        return os.path.isfile(self.table_file_path)

    def remove_table_file(self):
        """Remove the `table_file_path` file from the file system if it exists."""
        if (self.table_file_path is not None) and self.is_table_file_exist():
            os.remove(self.table_file_path)

    def load_table(self, node_class: Type[NodeT]):
        """Load the table from `table_file_path` file.

        This method replays the state of the table from local file,
        deserializing each line to a file node. Later file node entries will overwrite
        earlier ones to ensure the table contains the latest file states.
        """
        if self.table_file_path is None:
            return
        if not self.is_table_file_exist():
            return
        with open(self.table_file_path, "r") as f:
            for line in f.readlines():
                _file_node = node_class.deserialize(line)
                # let later entries overwrite earlier entries
                self.table[_file_node.file_path] = _file_node


class UploadCompletionTable(BaseCompletionTable[UploadFileNode]):
    """A class for managing the upload completion table for file nodes during file upload.

    This class specializes the BaseCompletionTable for managing upload-specific file nodes.
    """

    def create_file_node(self, fp) -> UploadFileNode:
        """Create an upload file node for the given file path.

        This method creates an upload file node based on the file path, size,
        last modified time, and partition count, then adds this entry to the table.
        """
        if not os.path.isfile(fp):
            # normal workflow should never get here
            raise NgcException(f"File path: {fp} which used to create file index is invalid.")

        _file_size = os.path.getsize(fp)
        number_of_file_partitions = (_file_size - 1) // PARTITION_SIZE + 1

        self.table[fp] = UploadFileNode(
            file_path=fp, size=_file_size, ftime=os.path.getmtime(fp), bitmask=2**number_of_file_partitions - 1
        )
        return self.table[fp]

    def load_table(self):
        """Load the table of upload file nodes from the `table_file_path` file."""
        super().load_table(UploadFileNode)


class DownloadCompletionTable(BaseCompletionTable[DownloadFileNode]):
    """A class for managing the download completion table for file nodes during file download.

    This class specializes the BaseCompletionTable for managing download-specific file nodes.
    """

    def create_file_node(self, fp) -> DownloadFileNode:
        """Create a download file node for the given file path."""
        raise NotImplementedError()

    def load_table(self):
        """Load the table of download file nodes from the `table_file_path` file."""
        super().load_table(DownloadFileNode)


class AsyncTransferWorkerPoolBase(ABC):
    """Base class for managing a pool of asynchronous transfer workers.

    This abstract base class defines the structure and common functionality
    for a worker pool that perform asynchronous file transfers. It handles
    the initialization of worker attributes, including artifact details,
    local directory, worker count, and coordination tables. All workers of
    the same worker type are coroutines of the same function.
    """

    def __init__(
        self,
        artifact_type: str,
        artifact_org: str,
        artifact_team: str,
        artifact_name: str,
        artifact_version: str,
        local_dir: str,
        worker_count: int,
        c_table: BaseCompletionTable,
        progress: Optional[AsyncTransferProgress] = None,
    ):
        self.consumers = []

        # every worker is going to get access to all the resources
        # writables should ensure safety

        # read-only
        self.base_url = add_scheme(NGC_CLI_API_URL)
        self.artifact_type = artifact_type
        self.artifact_org = artifact_org
        self.artifact_team = artifact_team
        self.artifact_name = artifact_name
        self.artifact_version = artifact_version

        self.local_dir = local_dir
        self.worker_count = worker_count

        # writables/executables cordinations required
        self.c_table = c_table
        self.progress = progress

        self.queue: asyncio.Queue
        self.auth_lock: asyncio.Lock
        self.executor: ProcessPoolExecutor
        self.session: aiohttp.ClientSession

    @property
    @abstractmethod
    def worker_type(self) -> str:
        """Abstract read-only property that must be implemented by subclasses."""

    async def make_auth_headers(self):
        """Create authentication headers for API requests."""
        async with self.auth_lock:
            return Authentication.auth_header(auth_org=self.artifact_org, auth_team=self.artifact_team)

    async def file_reader(self, file_path, start, end) -> AsyncGenerator[bytes, None]:
        """Read a file asynchronously in chunks."""
        try:
            async with aiofiles.open(file_path, "rb", buffering=0) as f:
                await f.seek(start)
                for _ in range((end - start) // NGC_CLI_TRANSFER_CHUNK_SIZE):
                    yield await f.read(NGC_CLI_TRANSFER_CHUNK_SIZE)
                yield await f.read((end - start) % NGC_CLI_TRANSFER_CHUNK_SIZE)
        except asyncio.CancelledError:
            await f.close()
            log_debug(self.worker_type, "cancel", f"canceled file_reader {file_path,start,end}, reraise")
            raise

    async def fetch_workload(self) -> Tuple[Any, ...]:
        """Fetch a workload from the queue."""
        return await self.queue.get()

    async def dispatch_workload(self, workload: Tuple[Any, ...]):
        """Dispatch a workload to consumer workerpools' queue."""
        if not self.consumers:
            raise NgcException(f"{self.worker_type} is a leaf in the consumer tree.")
        for consumer in self.consumers:
            await consumer.queue.put(workload)
            log_debug(
                self.worker_type,
                "queue",
                f"Queue to {consumer.worker_type} workload: [{workload}]",
            )

    @abstractmethod
    async def process_workload(self, workload: Tuple):
        """Process a workload.

        Abstract method that must be implemented by subclasses to define how
        a workload should be processed. This method represents the core
        long-running work function for the worker.
        """

    async def long_running_work(self, worker_name):
        """Execute long-running work for a worker.

        Continuously fetches and processes workloads in an infinite loop until
        cancelled. Handles cancellation and other exceptions appropriately.
        Worker pools do not cancel by themselves, cancel after queue join
        to allow workloads to complete.
        """
        try:
            while True:
                await self.process_workload(await self.fetch_workload())
                self.queue.task_done()
        except asyncio.CancelledError:
            log_debug(f"{self.worker_type}", "exception", f"canceled worker {worker_name}, no reraise.")

        except Exception as e:
            log_debug(f"{self.worker_type}", "exception", f"{str(e)}--{type(e)}")
            raise e

    def get_upload_url(self):
        """Generate the URL for file uploads."""
        return (
            f"{self.base_url}/v2/org/{self.artifact_org}"
            + (f"/team/{self.artifact_team}" if self.artifact_team else "")
            + "/files/multipart"
        )

    def get_file_url(self, rel_path):
        """Generate the URL for accessing a file."""
        return "{}/v2/org/{}/{}{}/{}/versions/{}/files/{}".format(
            self.base_url,
            self.artifact_org,
            f"team/{self.artifact_team}/" if self.artifact_team else "",
            self.artifact_type,
            self.artifact_name,
            self.artifact_version,
            rel_path,
        )


class AsyncFilePreSignUrlWorkerPool(AsyncTransferWorkerPoolBase):
    """Handle the generation of pre-signed URLs for file uploads in an asynchronous worker pool.

    This class extends AsyncTransferWorkerPoolBase and is responsible for obtaining pre-signed URLs necessary for
    clients to upload files directly to AWS s3 without further authentication.
    """

    def __init__(
        self,
        artifact_type: str,
        artifact_org: str,
        artifact_team: str,
        artifact_name: str,
        artifact_version: str,
        local_dir: str,
        worker_count: int,
        c_table: UploadCompletionTable,
        progress: Optional[AsyncTransferProgress] = None,
    ):
        super().__init__(
            artifact_type,
            artifact_org,
            artifact_team,
            artifact_name,
            artifact_version,
            local_dir,
            worker_count,
            c_table,
            progress,
        )
        self.queue: asyncio.Queue[Tuple[str]]

    @property
    def worker_type(self) -> str:
        """Return the type of worker."""
        return "file-worker"

    async def process_workload(self, workload: Tuple[str]):
        """Process a workload by generating pre-signed URLs for file parts.

        Extracts a file path from the workload and retrieves its progress from completion table.
        If all file parts are uploaded, it skips processing.
        Otherwise, it requests pre-signed URLs for the incomplete parts and dispatches
        pre-signed URLs to cusomer worker pool (upload-worker) queue.
        """
        (file_path,) = workload

        file_node = self.c_table.get_file_node(file_path)
        assert file_node is not None

        # If all file partitions are uploaded, nothing to do by this worker
        # If this file needs to be marked complete, hash worker will send it
        if file_node.bitmask == 0:
            log_debug(self.worker_type, "complete", f"{file_path} all parts uploaded,omit here in pre-sign-url-request")

        # If not all file partitions are upload,
        # get uncompleted part_numbers and request pre-signed urls for partnumbers only
        else:
            part_numbers = [  # part numbers are 1 indexed
                idx + 1 for idx in bitmask_get_set_bits(file_node.bitmask, (file_node.size - 1) // PARTITION_SIZE + 1)
            ]
            try:
                resp_json = await self._request_file_upload_urls(
                    file_path, file_node.size, file_node.upload_id, part_numbers
                )
                # Async GAP on resume: If only requested pre-signed urls but got interrupted here. No impact.
                # On resume, it is ok to forget the old upload_id and request a new one.
                # Partially uploaded, it is ok to request new pre-signed urls for incompleted partitions.
                urls = resp_json["urls"]
                upload_id = resp_json["uploadID"]
                file_node.upload_id = upload_id
                for idx, url in zip(part_numbers, urls):
                    await self.dispatch_workload((file_path, idx - 1, url))  # response partnumbers are also 1 indexed

            except aiohttp.ClientError:
                _failed_size_in_bytes = bitmask_set_bit_in_size(file_node.bitmask, file_node.size, PARTITION_SIZE)
                if self.progress:

                    # fail only incompleted size if fails at this worker
                    await self.progress.fail(_failed_size_in_bytes, 1)
                log_debug(
                    self.worker_type,
                    "failure",
                    f"{file_path} request_file_upload_urls failed, mark failure",
                )

    @async_retry(exception_to_check=aiohttp.ClientError, tries=NGC_CLI_UPLOAD_RETRIES, delay=500, backoff=2)
    async def _request_file_upload_urls(
        self, file_path: str, size: int, upload_id: Union[str, None], part_numbers: List[int]
    ) -> Dict[str, Union[str, List[str]]]:
        """Request pre-signed URLs for file uploads.

        Sends an HTTP POST request to obtain pre-signed URLs for uploading file parts,
        by agreed parition size PARTITION_SIZE.
        The request includes details such as the file path, size, upload ID, and part numbers.
        """
        body = {
            "name": self.artifact_name,
            "version": self.artifact_version,
            "artifactType": self.artifact_type,
            "filePath": os.path.relpath(file_path, self.local_dir),
            "size": size,
        }
        if upload_id:  # resuming an upload
            body["uploadID"] = upload_id
            if part_numbers:  # provide partitions IDs 1-indexed
                body["partNumberList"] = part_numbers

        response = await self.session.post(
            url=self.get_upload_url(),
            json=body,
            headers=await self.make_auth_headers(),
        )
        resp_json = await response.json(content_type="application/json")
        log_debug(
            self.worker_type,
            "_request_file_upload_urls",
            f"{response.status} - {file_path}, {upload_id}, {self.artifact_type} " + str(resp_json),
        )

        response.raise_for_status()
        return resp_json


class AsyncFileS3UploadWorkerPool(AsyncTransferWorkerPoolBase):
    """Manage the direct upload of files to AWS S3 storage using pre-signed URLs.

    This class is part of the asynchronous transfer worker pool and deals with
    the actual transfer of file partitions to the cloud, managing retries
    and handling upload failures.
    """

    def __init__(
        self,
        artifact_type: str,
        artifact_org: str,
        artifact_team: str,
        artifact_name: str,
        artifact_version: str,
        local_dir: str,
        worker_count: int,
        c_table: UploadCompletionTable,
        progress: Optional[AsyncTransferProgress] = None,
    ):
        super().__init__(
            artifact_type,
            artifact_org,
            artifact_team,
            artifact_name,
            artifact_version,
            local_dir,
            worker_count,
            c_table,
            progress,
        )

        self.c_table: UploadCompletionTable
        self.queue: asyncio.Queue[Tuple[str, int, str]]

    @property
    def worker_type(self) -> str:
        """Return the type of worker."""
        return "upload-worker"

    async def process_workload(self, workload: Tuple[str, int, str]):
        """Process a workload by uploading a file partition to S3.

        Extracts the file path, partition index, and pre-signed URL from the workload.
        Uploads the specified partition to S3 and updates the completion table.
        Handles client errors and logs failures appropriately.
        """
        (file_path, idx, url) = workload

        file_node = self.c_table.get_file_node(file_path)
        assert file_node is not None
        assert bitmask_is_bit_set(file_node.bitmask, idx), "Partition already complete"

        start = PARTITION_SIZE * idx
        end = min(PARTITION_SIZE + start, file_node.size)
        try:
            await self._request_s3_upload(file_path, start, end, url)
            # Async GAP on resume: If partition is upload succeeded but interrupted here. No impact
            # It is ok to request url for this partition and reupload
            await file_node.set_partition_complete(idx)
            if self.progress:
                await self.progress.advance(size_in_bytes=end - start, count=0)
            log_debug(
                self.worker_type,
                "complete",
                f"{file_path}:{idx} completed partition upload.",
            )
            if await file_node.set_race_flag_once():
                await self.dispatch_workload((file_path,))
        except aiohttp.ClientError as e:
            if self.progress:
                await self.progress.fail(end - start, (await file_node.set_failed_once()) * 1)
            log_debug(self.worker_type, "failure", f"{file_path}:{idx} upload failure {str(e)}")

    @async_retry(exception_to_check=aiohttp.ClientError, tries=NGC_CLI_UPLOAD_RETRIES, delay=500, backoff=2)
    async def _request_s3_upload(self, file_path, start, end, url):
        """Upload a file partition to S3.

        Sends an HTTP PUT request to upload a range of file bytes to S3 using the provided pre-signed URL.
        Manages retries and handles HTTP errors.
        """
        response = await self.session.put(
            url, data=self.file_reader(file_path, start, end), headers={"Content-Length": f"{end-start}"}
        )
        log_debug(
            self.worker_type,
            "_request_s3_upload",
            f"{response.status} - {file_path},  partition [{start},{end}], [{url}] ",
        )
        # s3 does not respond with a body
        response.raise_for_status()


def hash_file(file_path: str) -> str:
    """Calculate the SHA-256 hash of a file and returns it as a base64 encoded string.

    This function computes the SHA-256 hash of the specified file. It is designed to be
    pickleable so that it can be executed in a separate process using `run_in_executor`.
    """
    # on aynsio.task cancel, this subprocess will recieve SIGINT before we get to handle it
    # we want to this sub process to be terminated from main process gracefully
    # ignore sigint here and call shutdown() from main process
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    sha256_bstr: bytes = get_sha256_file_checksum(file_path)
    return base64.b64encode(sha256_bstr).decode("utf-8")


class AsyncFileHashWorkerPool(AsyncTransferWorkerPoolBase):
    """Responsible for computing the hash of files utilizing multiprocessing to verify integrity post-transfer.

    This worker is part of the asynchronous transfer worker pool and uses processpoolexecutors,
    wrapped by coroutines to perform computationally intensive hashing operations
    without blocking the main asynchronous event loop.
    """

    def __init__(
        self,
        artifact_type: str,
        artifact_org: str,
        artifact_team: str,
        artifact_name: str,
        artifact_version: str,
        local_dir: str,
        worker_count: int,
        c_table: UploadCompletionTable,
        progress: Optional[AsyncTransferProgress] = None,
    ):
        super().__init__(
            artifact_type,
            artifact_org,
            artifact_team,
            artifact_name,
            artifact_version,
            local_dir,
            worker_count,
            c_table,
            progress,
        )
        self.queue: asyncio.Queue[Tuple[str]]

    @property
    def worker_type(self) -> str:
        """Return the type of worker."""
        return "hash-worker"

    async def process_workload(self, workload: Tuple[str]):
        """Process a workload by computing the hash of a file.

        Summary:
        Extracts a file path from the workload and retrieves its progress from the completion table.
        Computes the hash of the file if it is not already computed,
        using an external executor to avoid blocking the event loop.
        Logs the completion of the hashing operation and handles race conditions with the upload worker.
        """
        (file_path,) = workload

        file_node = self.c_table.get_file_node(file_path)
        assert file_node is not None

        if not file_node.hash:
            loop = asyncio.get_running_loop()
            _hash = await loop.run_in_executor(self.executor, hash_file, file_path)
            # Async GAP on resume: If interrupted, restart hashing from begining of content
            # Right now hash has to be done in one go, constraint discussed in design
            file_node.hash = _hash

        log_debug(self.worker_type, "complete", f"{file_path} completed hash {file_node.hash}")

        if await file_node.set_race_flag_once():  # race with upload worker
            await self.dispatch_workload((file_path,))  # if wins the race, this worker send to mark completion


class AsyncFileCompletionWorkerPool(AsyncTransferWorkerPoolBase):
    """Responsible for marking files as complete once all transfer operations are successfully.

    This worker ensures that file states are updated to reflect their completion status in the system.
    """

    def __init__(
        self,
        artifact_type: str,
        artifact_org: str,
        artifact_team: str,
        artifact_name: str,
        artifact_version: str,
        local_dir: str,
        worker_count: int,
        c_table: UploadCompletionTable,
        progress: Optional[AsyncTransferProgress] = None,
    ):
        super().__init__(
            artifact_type,
            artifact_org,
            artifact_team,
            artifact_name,
            artifact_version,
            local_dir,
            worker_count,
            c_table,
            progress,
        )
        self.queue: asyncio.Queue[Tuple[str]]

    @property
    def worker_type(self) -> str:
        """Return the type of worker."""
        return "completion-worker"

    async def process_workload(self, workload: Tuple[str]):
        """Process a workload by marking a file as complete.

        Extracts the file path from the workload and retrieves its progress from the completion table.
        Marks the file as complete in the system once all parts are successfully uploaded and verified.
        """
        (file_path,) = workload
        file_node = self.c_table.get_file_node(file_path)
        assert file_node is not None

        try:
            await self._request_mark_complete(file_path, file_node.upload_id, file_node.hash)
            log_debug(self.worker_type, "complete", f"{file_path} done, note and pop")
            # Async GAP: If interrupted after marked complete suceeded, before writing to file node,
            # resume will retry completion, reuse the same upload_id which gets http 400 from BE
            # On http 400, check if file is already uploaded with _request_is_file_completed()
            await file_node.set_complete()
            if self.progress:
                await self.progress.advance(0, 1)
        except aiohttp.ClientError:
            if self.progress:
                await self.progress.fail(0, 1)
            log_debug(
                self.worker_type,
                "failure",
                f"{file_path} request_mark_complete failed, mark failure {file_node.upload_id}",
            )
        finally:
            await self.c_table.async_save_file_node(file_path)

    @async_retry(exception_to_check=aiohttp.ClientError, tries=NGC_CLI_UPLOAD_RETRIES, delay=500, backoff=2)
    async def _request_mark_complete(self, file_path, upload_id, chksum):
        """Send a request to mark a file as complete.

        Sends an HTTP PUT request to mark a file as complete for the BE to add entry. If the request fails
        with a 400 status, verifies if the file is already marked as complete.
        """
        body = {
            "name": self.artifact_name,
            "version": self.artifact_version,
            "artifactType": self.artifact_type,
            "filePath": os.path.relpath(file_path, self.local_dir),
            "uploadID": upload_id,
            "sha256": chksum,
        }
        response = await self.session.put(url=self.get_upload_url(), json=body, headers=await self.make_auth_headers())
        log_debug(
            self.worker_type,
            "_request_mark_complete",
            f"{response.status} - {file_path}, {upload_id}, {self.artifact_type} " + f" [{chksum}]",
        )

        if response.status != 200:
            log_debug(
                self.worker_type,
                "_request_mark_complete",
                f"{response.status} - {file_path}, {upload_id}, {self.artifact_type}"
                + str(await response.json(content_type="application/json")),
            )
            if response.status == 400:
                # see above `Async GAP`
                # make sure file is already uploaded by get_file
                return await self._request_is_file_completed(file_path)

        response.raise_for_status()

    @async_retry(exception_to_check=aiohttp.ClientError, tries=NGC_CLI_UPLOAD_RETRIES, delay=500, backoff=2)
    async def _request_is_file_completed(self, file_path):  # this is an edge case, not to be nested in retries
        """Verify if a file is already marked as complete.

        Sends an HTTP GET request to check if a file is downloadable(already marked as complete) in the system.
        This is used as a fallback check if the completion request fails with a 400 status.
        """
        log_debug(self.worker_type, "_request_is_file_completed", f"{file_path}")

        rel_path = os.path.relpath(file_path, self.local_dir)
        url = self.get_file_url(rel_path)

        response = await self.session.get(
            url=url,
            headers=await self.make_auth_headers(),
        )
        log_debug(
            self.worker_type,
            "_request_is_file_completed",
            f"{response.status} - {file_path}, {self.artifact_type},{url}",
        )  # do not want to log response content, response content is file in binary
        response.raise_for_status()
