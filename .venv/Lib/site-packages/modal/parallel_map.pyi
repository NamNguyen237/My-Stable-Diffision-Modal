import asyncio
import asyncio.events
import collections.abc
import enum
import modal._functions
import modal._utils.async_utils
import modal.client
import modal.functions
import modal.retries
import modal_proto.api_pb2
import typing
import typing_extensions

class _SynchronizedQueue:
    """mdmd:hidden"""
    async def init(self): ...
    async def put(self, item): ...
    async def get(self): ...

SUPERSELF = typing.TypeVar("SUPERSELF", covariant=True)

class SynchronizedQueue:
    """mdmd:hidden"""
    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    class __init_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /): ...
        async def aio(self, /): ...

    init: __init_spec[typing_extensions.Self]

    class __put_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /, item): ...
        async def aio(self, /, item): ...

    put: __put_spec[typing_extensions.Self]

    class __get_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /): ...
        async def aio(self, /): ...

    get: __get_spec[typing_extensions.Self]

class _OutputValue:
    """_OutputValue(value: Any)"""

    value: typing.Any

    def __init__(self, value: typing.Any) -> None:
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __repr__(self):
        """Return repr(self)."""
        ...

    def __eq__(self, other):
        """Return self==value."""
        ...

def _map_invocation(
    function: modal._functions._Function,
    raw_input_queue: _SynchronizedQueue,
    client: modal.client._Client,
    order_outputs: bool,
    return_exceptions: bool,
    wrap_returned_exceptions: bool,
    count_update_callback: typing.Optional[collections.abc.Callable[[int, int], None]],
    function_call_invocation_type: int,
): ...
def _map_helper(
    self: modal.functions.Function,
    async_input_gen: typing.AsyncGenerator[typing.Any, None],
    kwargs={},
    order_outputs: bool = True,
    return_exceptions: bool = False,
    wrap_returned_exceptions: bool = True,
) -> typing.AsyncGenerator[typing.Any, None]:
    """Core implementation that supports `_map_async()`, `_starmap_async()` and `_for_each_async()`.

    Runs in an event loop on the main thread. Concurrently feeds new input to the input queue and yields available
    outputs to the caller.

    Note that since the iterator(s) can block, it's a bit opaque how often the event
    loop decides to get a new input vs how often it will emit a new output.

    We could make this explicit as an improvement or even let users decide what they
    prefer: throughput (prioritize queueing inputs) or latency (prioritize yielding results)
    """
    ...

def _maybe_warn_about_exceptions(func_name: str, return_exceptions: bool, wrap_returned_exceptions: bool): ...
def _invoked_from_sync_wrapper() -> bool:
    """Check whether the calling function was called from a sync wrapper."""
    ...

def _map_async(
    self: modal.functions.Function,
    *input_iterators: typing.Union[typing.Iterable[typing.Any], typing.AsyncIterable[typing.Any]],
    kwargs={},
    order_outputs: bool = True,
    return_exceptions: bool = False,
    wrap_returned_exceptions: bool = True,
) -> typing.AsyncGenerator[typing.Any, None]: ...
def _starmap_async(
    self,
    input_iterator: typing.Union[
        typing.Iterable[typing.Sequence[typing.Any]], typing.AsyncIterable[typing.Sequence[typing.Any]]
    ],
    *,
    kwargs={},
    order_outputs: bool = True,
    return_exceptions: bool = False,
    wrap_returned_exceptions: bool = True,
) -> typing.AsyncIterable[typing.Any]: ...
async def _for_each_async(self, *input_iterators, kwargs={}, ignore_exceptions: bool = False) -> None: ...
def _map_sync(
    self,
    *input_iterators,
    kwargs={},
    order_outputs: bool = True,
    return_exceptions: bool = False,
    wrap_returned_exceptions: bool = True,
) -> modal._utils.async_utils.AsyncOrSyncIterable:
    """Parallel map over a set of inputs.

    Takes one iterator argument per argument in the function being mapped over.

    Example:
    ```python
    @app.function()
    def my_func(a):
        return a ** 2


    @app.local_entrypoint()
    def main():
        assert list(my_func.map([1, 2, 3, 4])) == [1, 4, 9, 16]
    ```

    If applied to a `app.function`, `map()` returns one result per input and the output order
    is guaranteed to be the same as the input order. Set `order_outputs=False` to return results
    in the order that they are completed instead.

    `return_exceptions` can be used to treat exceptions as successful results:

    ```python
    @app.function()
    def my_func(a):
        if a == 2:
            raise Exception("ohno")
        return a ** 2


    @app.local_entrypoint()
    def main():
        # [0, 1, UserCodeException(Exception('ohno'))]
        print(list(my_func.map(range(3), return_exceptions=True)))
    ```
    """
    ...

async def _spawn_map_async(self, *input_iterators, kwargs={}) -> None:
    """This runs in an event loop on the main thread. It consumes inputs from the input iterators and creates async
    function calls for each.
    """
    ...

def _spawn_map_sync(self, *input_iterators, kwargs={}) -> None:
    """Spawn parallel execution over a set of inputs, exiting as soon as the inputs are created (without waiting
    for the map to complete).

    Takes one iterator argument per argument in the function being mapped over.

    Example:
    ```python
    @app.function()
    def my_func(a):
        return a ** 2


    @app.local_entrypoint()
    def main():
        my_func.spawn_map([1, 2, 3, 4])
    ```

    Programmatic retrieval of results will be supported in a future update.
    """
    ...

def _for_each_sync(self, *input_iterators, kwargs={}, ignore_exceptions: bool = False):
    """Execute function for all inputs, ignoring outputs. Waits for completion of the inputs.

    Convenient alias for `.map()` in cases where the function just needs to be called.
    as the caller doesn't have to consume the generator to process the inputs.
    """
    ...

def _starmap_sync(
    self,
    input_iterator: typing.Iterable[typing.Sequence[typing.Any]],
    *,
    kwargs={},
    order_outputs: bool = True,
    return_exceptions: bool = False,
    wrap_returned_exceptions: bool = True,
) -> modal._utils.async_utils.AsyncOrSyncIterable:
    """Like `map`, but spreads arguments over multiple function arguments.

    Assumes every input is a sequence (e.g. a tuple).

    Example:
    ```python
    @app.function()
    def my_func(a, b):
        return a + b


    @app.local_entrypoint()
    def main():
        assert list(my_func.starmap([(1, 2), (3, 4)])) == [3, 7]
    ```
    """
    ...

class _MapItemState(enum.Enum):
    # The input is being sent the server with a PutInputs request, but the response has not been received yet.
    SENDING = 1
    # A call to either PutInputs or FunctionRetry has completed, and we are waiting to receive the output.
    WAITING_FOR_OUTPUT = 2
    # The input is on the retry queue, and waiting for its delay to expire.
    WAITING_TO_RETRY = 3
    # The input is being sent to the server with a FunctionRetry request, but the response has not been received yet.
    RETRYING = 4
    # The output has been received and was either successful, or failed with no more retries remaining.
    COMPLETE = 5

class _OutputType(enum.Enum):
    SUCCESSFUL_COMPLETION = 1
    FAILED_COMPLETION = 2
    RETRYING = 3
    ALREADY_COMPLETE_DUPLICATE = 4
    STALE_RETRY_DUPLICATE = 5
    NO_CONTEXT_DUPLICATE = 6

class _MapItemContext:
    state: _MapItemState
    input: modal_proto.api_pb2.FunctionInput
    retry_manager: modal.retries.RetryManager
    sync_client_retries_enabled: bool
    input_id: asyncio.Future
    input_jwt: asyncio.Future
    previous_input_jwt: typing.Optional[str]
    _event_loop: asyncio.events.AbstractEventLoop

    def __init__(
        self,
        input: modal_proto.api_pb2.FunctionInput,
        retry_manager: modal.retries.RetryManager,
        sync_client_retries_enabled: bool,
    ):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def handle_put_inputs_response(self, item: modal_proto.api_pb2.FunctionPutInputsResponseItem): ...
    async def handle_get_outputs_response(
        self,
        item: modal_proto.api_pb2.FunctionGetOutputsItem,
        now_seconds: int,
        function_call_invocation_type: int,
        retry_queue: modal._utils.async_utils.TimestampPriorityQueue,
    ) -> _OutputType:
        """Processes the output, and determines if it is complete or needs to be retried.

        Return True if input state was changed to COMPLETE, otherwise False.
        """
        ...

    async def prepare_item_for_retry(self) -> modal_proto.api_pb2.FunctionRetryInputsItem: ...
    def handle_retry_response(self, input_jwt: str): ...

class _MapItemsManager:
    def __init__(
        self,
        retry_policy: modal_proto.api_pb2.FunctionRetryPolicy,
        function_call_invocation_type: int,
        retry_queue: modal._utils.async_utils.TimestampPriorityQueue,
        sync_client_retries_enabled: bool,
        max_inputs_outstanding: int,
    ):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    async def add_items(self, items: list[modal_proto.api_pb2.FunctionPutInputsItem]): ...
    async def prepare_items_for_retry(
        self, retriable_idxs: list[int]
    ) -> list[modal_proto.api_pb2.FunctionRetryInputsItem]: ...
    def get_input_jwts_waiting_for_output(self) -> list[str]:
        """Returns a list of input_jwts for inputs that are waiting for output."""
        ...

    def _remove_item(self, item_idx: int): ...
    def get_item_context(self, item_idx: int) -> _MapItemContext: ...
    def handle_put_inputs_response(self, items: list[modal_proto.api_pb2.FunctionPutInputsResponseItem]): ...
    def handle_retry_response(self, input_jwts: list[str]): ...
    async def handle_get_outputs_response(
        self, item: modal_proto.api_pb2.FunctionGetOutputsItem, now_seconds: int
    ) -> _OutputType: ...
    def __len__(self): ...
