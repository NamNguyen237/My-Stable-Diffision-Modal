import collections.abc
import modal._object
import modal.client
import modal.object
import synchronicity.combined_types
import typing
import typing_extensions

def _serialize_dict(data): ...

class _Dict(modal._object._Object):
    """Distributed dictionary for storage in Modal apps.

    Dict contents can be essentially any object so long as they can be serialized by
    `cloudpickle`. This includes other Modal objects. If writing and reading in different
    environments (eg., writing locally and reading remotely), it's necessary to have the
    library defining the data type installed, with compatible versions, on both sides.
    Additionally, cloudpickle serialization is not guaranteed to be deterministic, so it is
    generally recommended to use primitive types for keys.

    **Lifetime of a Dict and its items**

    An individual Dict entry will expire after 7 days of inactivity (no reads or writes). The
    Dict entries are written to durable storage.

    Legacy Dicts (created before 2025-05-20) will still have entries expire 30 days after being
    last added. Additionally, contents are stored in memory on the Modal server and could be lost
    due to unexpected server restarts. Eventually, these Dicts will be fully sunset.

    **Usage**

    ```python
    from modal import Dict

    my_dict = Dict.from_name("my-persisted_dict", create_if_missing=True)

    my_dict["some key"] = "some value"
    my_dict[123] = 456

    assert my_dict["some key"] == "some value"
    assert my_dict[123] == 456
    ```

    The `Dict` class offers a few methods for operations that are usually accomplished
    in Python with operators, such as `Dict.put` and `Dict.contains`. The advantage of
    these methods is that they can be safely called in an asynchronous context by using
    the `.aio` suffix on the method, whereas their operator-based analogues will always
    run synchronously and block the event loop.

    For more examples, see the [guide](https://modal.com/docs/guide/dicts-and-queues#modal-dicts).
    """
    def __init__(self, data={}):
        """mdmd:hidden"""
        ...

    @classmethod
    def ephemeral(
        cls: type[_Dict],
        data: typing.Optional[dict] = None,
        client: typing.Optional[modal.client._Client] = None,
        environment_name: typing.Optional[str] = None,
        _heartbeat_sleep: float = 300,
    ) -> typing.AsyncContextManager[_Dict]:
        """Creates a new ephemeral Dict within a context manager:

        Usage:
        ```python
        from modal import Dict

        with Dict.ephemeral() as d:
            d["foo"] = "bar"
        ```

        ```python notest
        async with Dict.ephemeral() as d:
            await d.put.aio("foo", "bar")
        ```
        """
        ...

    @staticmethod
    def from_name(
        name: str,
        data: typing.Optional[dict] = None,
        *,
        namespace=1,
        environment_name: typing.Optional[str] = None,
        create_if_missing: bool = False,
    ) -> _Dict:
        """Reference a named Dict, creating if necessary.

        This is a lazy method that defers hydrating the local
        object with metadata from Modal servers until the first
        time it is actually used.

        ```python
        d = modal.Dict.from_name("my-dict", create_if_missing=True)
        d[123] = 456
        ```
        """
        ...

    @staticmethod
    async def lookup(
        name: str,
        data: typing.Optional[dict] = None,
        namespace=1,
        client: typing.Optional[modal.client._Client] = None,
        environment_name: typing.Optional[str] = None,
        create_if_missing: bool = False,
    ) -> _Dict:
        """mdmd:hidden
        Lookup a named Dict.

        DEPRECATED: This method is deprecated in favor of `modal.Dict.from_name`.

        In contrast to `modal.Dict.from_name`, this is an eager method
        that will hydrate the local object with metadata from Modal servers.

        ```python
        d = modal.Dict.from_name("my-dict")
        d["xyz"] = 123
        ```
        """
        ...

    @staticmethod
    async def delete(
        name: str,
        *,
        client: typing.Optional[modal.client._Client] = None,
        environment_name: typing.Optional[str] = None,
    ): ...
    async def clear(self) -> None:
        """Remove all items from the Dict."""
        ...

    async def get(self, key: typing.Any, default: typing.Optional[typing.Any] = None) -> typing.Any:
        """Get the value associated with a key.

        Returns `default` if key does not exist.
        """
        ...

    async def contains(self, key: typing.Any) -> bool:
        """Return if a key is present."""
        ...

    async def len(self) -> int:
        """Return the length of the Dict.

        Note: This is an expensive operation and will return at most 100,000.
        """
        ...

    async def __getitem__(self, key: typing.Any) -> typing.Any:
        """Get the value associated with a key.

        Note: this function will block the event loop when called in an async context.
        """
        ...

    async def update(self, other: typing.Optional[collections.abc.Mapping] = None, /, **kwargs) -> None:
        """Update the Dict with additional items."""
        ...

    async def put(self, key: typing.Any, value: typing.Any, *, skip_if_exists: bool = False) -> bool:
        """Add a specific key-value pair to the Dict.

        Returns True if the key-value pair was added and False if it wasn't because the key already existed and
        `skip_if_exists` was set.
        """
        ...

    async def __setitem__(self, key: typing.Any, value: typing.Any) -> None:
        """Set a specific key-value pair to the Dict.

        Note: this function will block the event loop when called in an async context.
        """
        ...

    async def pop(self, key: typing.Any) -> typing.Any:
        """Remove a key from the Dict, returning the value if it exists."""
        ...

    async def __delitem__(self, key: typing.Any) -> typing.Any:
        """Delete a key from the Dict.

        Note: this function will block the event loop when called in an async context.
        """
        ...

    async def __contains__(self, key: typing.Any) -> bool:
        """Return if a key is present.

        Note: this function will block the event loop when called in an async context.
        """
        ...

    def keys(self) -> collections.abc.AsyncIterator[typing.Any]:
        """Return an iterator over the keys in this Dict.

        Note that (unlike with Python dicts) the return value is a simple iterator,
        and results are unordered.
        """
        ...

    def values(self) -> collections.abc.AsyncIterator[typing.Any]:
        """Return an iterator over the values in this Dict.

        Note that (unlike with Python dicts) the return value is a simple iterator,
        and results are unordered.
        """
        ...

    def items(self) -> collections.abc.AsyncIterator[tuple[typing.Any, typing.Any]]:
        """Return an iterator over the (key, value) tuples in this Dict.

        Note that (unlike with Python dicts) the return value is a simple iterator,
        and results are unordered.
        """
        ...

SUPERSELF = typing.TypeVar("SUPERSELF", covariant=True)

class Dict(modal.object.Object):
    """Distributed dictionary for storage in Modal apps.

    Dict contents can be essentially any object so long as they can be serialized by
    `cloudpickle`. This includes other Modal objects. If writing and reading in different
    environments (eg., writing locally and reading remotely), it's necessary to have the
    library defining the data type installed, with compatible versions, on both sides.
    Additionally, cloudpickle serialization is not guaranteed to be deterministic, so it is
    generally recommended to use primitive types for keys.

    **Lifetime of a Dict and its items**

    An individual Dict entry will expire after 7 days of inactivity (no reads or writes). The
    Dict entries are written to durable storage.

    Legacy Dicts (created before 2025-05-20) will still have entries expire 30 days after being
    last added. Additionally, contents are stored in memory on the Modal server and could be lost
    due to unexpected server restarts. Eventually, these Dicts will be fully sunset.

    **Usage**

    ```python
    from modal import Dict

    my_dict = Dict.from_name("my-persisted_dict", create_if_missing=True)

    my_dict["some key"] = "some value"
    my_dict[123] = 456

    assert my_dict["some key"] == "some value"
    assert my_dict[123] == 456
    ```

    The `Dict` class offers a few methods for operations that are usually accomplished
    in Python with operators, such as `Dict.put` and `Dict.contains`. The advantage of
    these methods is that they can be safely called in an asynchronous context by using
    the `.aio` suffix on the method, whereas their operator-based analogues will always
    run synchronously and block the event loop.

    For more examples, see the [guide](https://modal.com/docs/guide/dicts-and-queues#modal-dicts).
    """
    def __init__(self, data={}):
        """mdmd:hidden"""
        ...

    @classmethod
    def ephemeral(
        cls: type[Dict],
        data: typing.Optional[dict] = None,
        client: typing.Optional[modal.client.Client] = None,
        environment_name: typing.Optional[str] = None,
        _heartbeat_sleep: float = 300,
    ) -> synchronicity.combined_types.AsyncAndBlockingContextManager[Dict]:
        """Creates a new ephemeral Dict within a context manager:

        Usage:
        ```python
        from modal import Dict

        with Dict.ephemeral() as d:
            d["foo"] = "bar"
        ```

        ```python notest
        async with Dict.ephemeral() as d:
            await d.put.aio("foo", "bar")
        ```
        """
        ...

    @staticmethod
    def from_name(
        name: str,
        data: typing.Optional[dict] = None,
        *,
        namespace=1,
        environment_name: typing.Optional[str] = None,
        create_if_missing: bool = False,
    ) -> Dict:
        """Reference a named Dict, creating if necessary.

        This is a lazy method that defers hydrating the local
        object with metadata from Modal servers until the first
        time it is actually used.

        ```python
        d = modal.Dict.from_name("my-dict", create_if_missing=True)
        d[123] = 456
        ```
        """
        ...

    class __lookup_spec(typing_extensions.Protocol):
        def __call__(
            self,
            /,
            name: str,
            data: typing.Optional[dict] = None,
            namespace=1,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
            create_if_missing: bool = False,
        ) -> Dict:
            """mdmd:hidden
            Lookup a named Dict.

            DEPRECATED: This method is deprecated in favor of `modal.Dict.from_name`.

            In contrast to `modal.Dict.from_name`, this is an eager method
            that will hydrate the local object with metadata from Modal servers.

            ```python
            d = modal.Dict.from_name("my-dict")
            d["xyz"] = 123
            ```
            """
            ...

        async def aio(
            self,
            /,
            name: str,
            data: typing.Optional[dict] = None,
            namespace=1,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
            create_if_missing: bool = False,
        ) -> Dict:
            """mdmd:hidden
            Lookup a named Dict.

            DEPRECATED: This method is deprecated in favor of `modal.Dict.from_name`.

            In contrast to `modal.Dict.from_name`, this is an eager method
            that will hydrate the local object with metadata from Modal servers.

            ```python
            d = modal.Dict.from_name("my-dict")
            d["xyz"] = 123
            ```
            """
            ...

    lookup: __lookup_spec

    class __delete_spec(typing_extensions.Protocol):
        def __call__(
            self,
            /,
            name: str,
            *,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
        ): ...
        async def aio(
            self,
            /,
            name: str,
            *,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
        ): ...

    delete: __delete_spec

    class __clear_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /) -> None:
            """Remove all items from the Dict."""
            ...

        async def aio(self, /) -> None:
            """Remove all items from the Dict."""
            ...

    clear: __clear_spec[typing_extensions.Self]

    class __get_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /, key: typing.Any, default: typing.Optional[typing.Any] = None) -> typing.Any:
            """Get the value associated with a key.

            Returns `default` if key does not exist.
            """
            ...

        async def aio(self, /, key: typing.Any, default: typing.Optional[typing.Any] = None) -> typing.Any:
            """Get the value associated with a key.

            Returns `default` if key does not exist.
            """
            ...

    get: __get_spec[typing_extensions.Self]

    class __contains_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /, key: typing.Any) -> bool:
            """Return if a key is present."""
            ...

        async def aio(self, /, key: typing.Any) -> bool:
            """Return if a key is present."""
            ...

    contains: __contains_spec[typing_extensions.Self]

    class __len_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /) -> int:
            """Return the length of the Dict.

            Note: This is an expensive operation and will return at most 100,000.
            """
            ...

        async def aio(self, /) -> int:
            """Return the length of the Dict.

            Note: This is an expensive operation and will return at most 100,000.
            """
            ...

    len: __len_spec[typing_extensions.Self]

    class ____getitem___spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /, key: typing.Any) -> typing.Any:
            """Get the value associated with a key.

            Note: this function will block the event loop when called in an async context.
            """
            ...

        async def aio(self, /, key: typing.Any) -> typing.Any:
            """Get the value associated with a key.

            Note: this function will block the event loop when called in an async context.
            """
            ...

    __getitem__: ____getitem___spec[typing_extensions.Self]

    class __update_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, other: typing.Optional[collections.abc.Mapping] = None, /, **kwargs) -> None:
            """Update the Dict with additional items."""
            ...

        async def aio(self, other: typing.Optional[collections.abc.Mapping] = None, /, **kwargs) -> None:
            """Update the Dict with additional items."""
            ...

    update: __update_spec[typing_extensions.Self]

    class __put_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /, key: typing.Any, value: typing.Any, *, skip_if_exists: bool = False) -> bool:
            """Add a specific key-value pair to the Dict.

            Returns True if the key-value pair was added and False if it wasn't because the key already existed and
            `skip_if_exists` was set.
            """
            ...

        async def aio(self, /, key: typing.Any, value: typing.Any, *, skip_if_exists: bool = False) -> bool:
            """Add a specific key-value pair to the Dict.

            Returns True if the key-value pair was added and False if it wasn't because the key already existed and
            `skip_if_exists` was set.
            """
            ...

    put: __put_spec[typing_extensions.Self]

    class ____setitem___spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /, key: typing.Any, value: typing.Any) -> None:
            """Set a specific key-value pair to the Dict.

            Note: this function will block the event loop when called in an async context.
            """
            ...

        async def aio(self, /, key: typing.Any, value: typing.Any) -> None:
            """Set a specific key-value pair to the Dict.

            Note: this function will block the event loop when called in an async context.
            """
            ...

    __setitem__: ____setitem___spec[typing_extensions.Self]

    class __pop_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /, key: typing.Any) -> typing.Any:
            """Remove a key from the Dict, returning the value if it exists."""
            ...

        async def aio(self, /, key: typing.Any) -> typing.Any:
            """Remove a key from the Dict, returning the value if it exists."""
            ...

    pop: __pop_spec[typing_extensions.Self]

    class ____delitem___spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /, key: typing.Any) -> typing.Any:
            """Delete a key from the Dict.

            Note: this function will block the event loop when called in an async context.
            """
            ...

        async def aio(self, /, key: typing.Any) -> typing.Any:
            """Delete a key from the Dict.

            Note: this function will block the event loop when called in an async context.
            """
            ...

    __delitem__: ____delitem___spec[typing_extensions.Self]

    class ____contains___spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /, key: typing.Any) -> bool:
            """Return if a key is present.

            Note: this function will block the event loop when called in an async context.
            """
            ...

        async def aio(self, /, key: typing.Any) -> bool:
            """Return if a key is present.

            Note: this function will block the event loop when called in an async context.
            """
            ...

    __contains__: ____contains___spec[typing_extensions.Self]

    class __keys_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /) -> typing.Iterator[typing.Any]:
            """Return an iterator over the keys in this Dict.

            Note that (unlike with Python dicts) the return value is a simple iterator,
            and results are unordered.
            """
            ...

        def aio(self, /) -> collections.abc.AsyncIterator[typing.Any]:
            """Return an iterator over the keys in this Dict.

            Note that (unlike with Python dicts) the return value is a simple iterator,
            and results are unordered.
            """
            ...

    keys: __keys_spec[typing_extensions.Self]

    class __values_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /) -> typing.Iterator[typing.Any]:
            """Return an iterator over the values in this Dict.

            Note that (unlike with Python dicts) the return value is a simple iterator,
            and results are unordered.
            """
            ...

        def aio(self, /) -> collections.abc.AsyncIterator[typing.Any]:
            """Return an iterator over the values in this Dict.

            Note that (unlike with Python dicts) the return value is a simple iterator,
            and results are unordered.
            """
            ...

    values: __values_spec[typing_extensions.Self]

    class __items_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /) -> typing.Iterator[tuple[typing.Any, typing.Any]]:
            """Return an iterator over the (key, value) tuples in this Dict.

            Note that (unlike with Python dicts) the return value is a simple iterator,
            and results are unordered.
            """
            ...

        def aio(self, /) -> collections.abc.AsyncIterator[tuple[typing.Any, typing.Any]]:
            """Return an iterator over the (key, value) tuples in this Dict.

            Note that (unlike with Python dicts) the return value is a simple iterator,
            and results are unordered.
            """
            ...

    items: __items_spec[typing_extensions.Self]
