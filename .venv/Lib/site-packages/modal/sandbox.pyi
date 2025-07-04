import _typeshed
import collections.abc
import google.protobuf.message
import modal._object
import modal._tunnel
import modal.app
import modal.client
import modal.cloud_bucket_mount
import modal.container_process
import modal.file_io
import modal.gpu
import modal.image
import modal.io_streams
import modal.mount
import modal.network_file_system
import modal.object
import modal.proxy
import modal.scheduler_placement
import modal.secret
import modal.snapshot
import modal.stream_type
import modal.volume
import modal_proto.api_pb2
import os
import typing
import typing_extensions

def _validate_exec_args(entrypoint_args: collections.abc.Sequence[str]) -> None: ...

class _Sandbox(modal._object._Object):
    """A `Sandbox` object lets you interact with a running sandbox. This API is similar to Python's
    [asyncio.subprocess.Process](https://docs.python.org/3/library/asyncio-subprocess.html#asyncio.subprocess.Process).

    Refer to the [guide](https://modal.com/docs/guide/sandbox) on how to spawn and use sandboxes.
    """

    _result: typing.Optional[modal_proto.api_pb2.GenericResult]
    _stdout: modal.io_streams._StreamReader[str]
    _stderr: modal.io_streams._StreamReader[str]
    _stdin: modal.io_streams._StreamWriter
    _task_id: typing.Optional[str]
    _tunnels: typing.Optional[dict[int, modal._tunnel.Tunnel]]
    _enable_snapshot: bool

    @staticmethod
    def _new(
        entrypoint_args: collections.abc.Sequence[str],
        image: modal.image._Image,
        secrets: collections.abc.Sequence[modal.secret._Secret],
        timeout: typing.Optional[int] = None,
        workdir: typing.Optional[str] = None,
        gpu: typing.Union[None, str, modal.gpu._GPUConfig] = None,
        cloud: typing.Optional[str] = None,
        region: typing.Union[str, collections.abc.Sequence[str], None] = None,
        cpu: typing.Optional[float] = None,
        memory: typing.Union[int, tuple[int, int], None] = None,
        mounts: collections.abc.Sequence[modal.mount._Mount] = (),
        network_file_systems: dict[typing.Union[str, os.PathLike], modal.network_file_system._NetworkFileSystem] = {},
        block_network: bool = False,
        cidr_allowlist: typing.Optional[collections.abc.Sequence[str]] = None,
        volumes: dict[
            typing.Union[str, os.PathLike],
            typing.Union[modal.volume._Volume, modal.cloud_bucket_mount._CloudBucketMount],
        ] = {},
        pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
        encrypted_ports: collections.abc.Sequence[int] = [],
        h2_ports: collections.abc.Sequence[int] = [],
        unencrypted_ports: collections.abc.Sequence[int] = [],
        proxy: typing.Optional[modal.proxy._Proxy] = None,
        _experimental_scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
        enable_snapshot: bool = False,
        verbose: bool = False,
    ) -> _Sandbox:
        """mdmd:hidden"""
        ...

    @staticmethod
    async def create(
        *entrypoint_args: str,
        app: typing.Optional[modal.app._App] = None,
        environment_name: typing.Optional[str] = None,
        image: typing.Optional[modal.image._Image] = None,
        secrets: collections.abc.Sequence[modal.secret._Secret] = (),
        network_file_systems: dict[typing.Union[str, os.PathLike], modal.network_file_system._NetworkFileSystem] = {},
        timeout: typing.Optional[int] = None,
        workdir: typing.Optional[str] = None,
        gpu: typing.Union[None, str, modal.gpu._GPUConfig] = None,
        cloud: typing.Optional[str] = None,
        region: typing.Union[str, collections.abc.Sequence[str], None] = None,
        cpu: typing.Union[float, tuple[float, float], None] = None,
        memory: typing.Union[int, tuple[int, int], None] = None,
        block_network: bool = False,
        cidr_allowlist: typing.Optional[collections.abc.Sequence[str]] = None,
        volumes: dict[
            typing.Union[str, os.PathLike],
            typing.Union[modal.volume._Volume, modal.cloud_bucket_mount._CloudBucketMount],
        ] = {},
        pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
        encrypted_ports: collections.abc.Sequence[int] = [],
        h2_ports: collections.abc.Sequence[int] = [],
        unencrypted_ports: collections.abc.Sequence[int] = [],
        proxy: typing.Optional[modal.proxy._Proxy] = None,
        verbose: bool = False,
        _experimental_enable_snapshot: bool = False,
        _experimental_scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
        client: typing.Optional[modal.client._Client] = None,
    ) -> _Sandbox:
        """Create a new Sandbox to run untrusted, arbitrary code. The Sandbox's corresponding container
        will be created asynchronously.

        **Usage**

        ```python
        app = modal.App.lookup('sandbox-hello-world', create_if_missing=True)
        sandbox = modal.Sandbox.create("echo", "hello world", app=app)
        print(sandbox.stdout.read())
        sandbox.wait()
        ```
        """
        ...

    @staticmethod
    async def _create(
        *entrypoint_args: str,
        app: typing.Optional[modal.app._App] = None,
        environment_name: typing.Optional[str] = None,
        image: typing.Optional[modal.image._Image] = None,
        secrets: collections.abc.Sequence[modal.secret._Secret] = (),
        mounts: collections.abc.Sequence[modal.mount._Mount] = (),
        network_file_systems: dict[typing.Union[str, os.PathLike], modal.network_file_system._NetworkFileSystem] = {},
        timeout: typing.Optional[int] = None,
        workdir: typing.Optional[str] = None,
        gpu: typing.Union[None, str, modal.gpu._GPUConfig] = None,
        cloud: typing.Optional[str] = None,
        region: typing.Union[str, collections.abc.Sequence[str], None] = None,
        cpu: typing.Union[float, tuple[float, float], None] = None,
        memory: typing.Union[int, tuple[int, int], None] = None,
        block_network: bool = False,
        cidr_allowlist: typing.Optional[collections.abc.Sequence[str]] = None,
        volumes: dict[
            typing.Union[str, os.PathLike],
            typing.Union[modal.volume._Volume, modal.cloud_bucket_mount._CloudBucketMount],
        ] = {},
        pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
        encrypted_ports: collections.abc.Sequence[int] = [],
        h2_ports: collections.abc.Sequence[int] = [],
        unencrypted_ports: collections.abc.Sequence[int] = [],
        proxy: typing.Optional[modal.proxy._Proxy] = None,
        _experimental_enable_snapshot: bool = False,
        _experimental_scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
        client: typing.Optional[modal.client._Client] = None,
        verbose: bool = False,
    ): ...
    def _hydrate_metadata(self, handle_metadata: typing.Optional[google.protobuf.message.Message]): ...
    @staticmethod
    async def from_id(sandbox_id: str, client: typing.Optional[modal.client._Client] = None) -> _Sandbox:
        """Construct a Sandbox from an id and look up the Sandbox result.

        The ID of a Sandbox object can be accessed using `.object_id`.
        """
        ...

    async def set_tags(self, tags: dict[str, str], *, client: typing.Optional[modal.client._Client] = None):
        """Set tags (key-value pairs) on the Sandbox. Tags can be used to filter results in `Sandbox.list`."""
        ...

    async def snapshot_filesystem(self, timeout: int = 55) -> modal.image._Image:
        """Snapshot the filesystem of the Sandbox.

        Returns an [`Image`](https://modal.com/docs/reference/modal.Image) object which
        can be used to spawn a new Sandbox with the same filesystem.
        """
        ...

    async def wait(self, raise_on_termination: bool = True):
        """Wait for the Sandbox to finish running."""
        ...

    async def tunnels(self, timeout: int = 50) -> dict[int, modal._tunnel.Tunnel]:
        """Get Tunnel metadata for the sandbox.

        Raises `SandboxTimeoutError` if the tunnels are not available after the timeout.

        Returns a dictionary of `Tunnel` objects which are keyed by the container port.

        NOTE: Previous to client [v0.64.153](https://modal.com/docs/reference/changelog#064153-2024-09-30), this
        returned a list of `TunnelData` objects.
        """
        ...

    async def terminate(self) -> None:
        """Terminate Sandbox execution.

        This is a no-op if the Sandbox has already finished running.
        """
        ...

    async def poll(self) -> typing.Optional[int]:
        """Check if the Sandbox has finished running.

        Returns `None` if the Sandbox is still running, else returns the exit code.
        """
        ...

    async def _get_task_id(self) -> str: ...
    @typing.overload
    async def exec(
        self,
        *cmds: str,
        pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
        stdout: modal.stream_type.StreamType = modal.stream_type.StreamType.PIPE,
        stderr: modal.stream_type.StreamType = modal.stream_type.StreamType.PIPE,
        timeout: typing.Optional[int] = None,
        workdir: typing.Optional[str] = None,
        secrets: collections.abc.Sequence[modal.secret._Secret] = (),
        text: typing.Literal[True] = True,
        bufsize: typing.Literal[-1, 1] = -1,
        _pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
    ) -> modal.container_process._ContainerProcess[str]: ...
    @typing.overload
    async def exec(
        self,
        *cmds: str,
        pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
        stdout: modal.stream_type.StreamType = modal.stream_type.StreamType.PIPE,
        stderr: modal.stream_type.StreamType = modal.stream_type.StreamType.PIPE,
        timeout: typing.Optional[int] = None,
        workdir: typing.Optional[str] = None,
        secrets: collections.abc.Sequence[modal.secret._Secret] = (),
        text: typing.Literal[False] = False,
        bufsize: typing.Literal[-1, 1] = -1,
        _pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
    ) -> modal.container_process._ContainerProcess[bytes]: ...
    async def _experimental_snapshot(self) -> modal.snapshot._SandboxSnapshot: ...
    @staticmethod
    async def _experimental_from_snapshot(
        snapshot: modal.snapshot._SandboxSnapshot, client: typing.Optional[modal.client._Client] = None
    ): ...
    @typing.overload
    async def open(self, path: str, mode: _typeshed.OpenTextMode) -> modal.file_io._FileIO[str]: ...
    @typing.overload
    async def open(self, path: str, mode: _typeshed.OpenBinaryMode) -> modal.file_io._FileIO[bytes]: ...
    async def ls(self, path: str) -> list[str]:
        """List the contents of a directory in the Sandbox."""
        ...

    async def mkdir(self, path: str, parents: bool = False) -> None:
        """Create a new directory in the Sandbox."""
        ...

    async def rm(self, path: str, recursive: bool = False) -> None:
        """Remove a file or directory in the Sandbox."""
        ...

    def watch(
        self,
        path: str,
        filter: typing.Optional[list[modal.file_io.FileWatchEventType]] = None,
        recursive: typing.Optional[bool] = None,
        timeout: typing.Optional[int] = None,
    ) -> typing.AsyncIterator[modal.file_io.FileWatchEvent]:
        """Watch a file or directory in the Sandbox for changes."""
        ...

    @property
    def stdout(self) -> modal.io_streams._StreamReader[str]:
        """[`StreamReader`](https://modal.com/docs/reference/modal.io_streams#modalio_streamsstreamreader) for
        the sandbox's stdout stream.
        """
        ...

    @property
    def stderr(self) -> modal.io_streams._StreamReader[str]:
        """[`StreamReader`](https://modal.com/docs/reference/modal.io_streams#modalio_streamsstreamreader) for
        the Sandbox's stderr stream.
        """
        ...

    @property
    def stdin(self) -> modal.io_streams._StreamWriter:
        """[`StreamWriter`](https://modal.com/docs/reference/modal.io_streams#modalio_streamsstreamwriter) for
        the Sandbox's stdin stream.
        """
        ...

    @property
    def returncode(self) -> typing.Optional[int]:
        """Return code of the Sandbox process if it has finished running, else `None`."""
        ...

    @staticmethod
    def list(
        *,
        app_id: typing.Optional[str] = None,
        tags: typing.Optional[dict[str, str]] = None,
        client: typing.Optional[modal.client._Client] = None,
    ) -> collections.abc.AsyncGenerator[_Sandbox, None]:
        """List all Sandboxes for the current Environment or App ID (if specified). If tags are specified, only
        Sandboxes that have at least those tags are returned. Returns an iterator over `Sandbox` objects.
        """
        ...

SUPERSELF = typing.TypeVar("SUPERSELF", covariant=True)

class Sandbox(modal.object.Object):
    """A `Sandbox` object lets you interact with a running sandbox. This API is similar to Python's
    [asyncio.subprocess.Process](https://docs.python.org/3/library/asyncio-subprocess.html#asyncio.subprocess.Process).

    Refer to the [guide](https://modal.com/docs/guide/sandbox) on how to spawn and use sandboxes.
    """

    _result: typing.Optional[modal_proto.api_pb2.GenericResult]
    _stdout: modal.io_streams.StreamReader[str]
    _stderr: modal.io_streams.StreamReader[str]
    _stdin: modal.io_streams.StreamWriter
    _task_id: typing.Optional[str]
    _tunnels: typing.Optional[dict[int, modal._tunnel.Tunnel]]
    _enable_snapshot: bool

    def __init__(self, *args, **kwargs):
        """mdmd:hidden"""
        ...

    @staticmethod
    def _new(
        entrypoint_args: collections.abc.Sequence[str],
        image: modal.image.Image,
        secrets: collections.abc.Sequence[modal.secret.Secret],
        timeout: typing.Optional[int] = None,
        workdir: typing.Optional[str] = None,
        gpu: typing.Union[None, str, modal.gpu._GPUConfig] = None,
        cloud: typing.Optional[str] = None,
        region: typing.Union[str, collections.abc.Sequence[str], None] = None,
        cpu: typing.Optional[float] = None,
        memory: typing.Union[int, tuple[int, int], None] = None,
        mounts: collections.abc.Sequence[modal.mount.Mount] = (),
        network_file_systems: dict[typing.Union[str, os.PathLike], modal.network_file_system.NetworkFileSystem] = {},
        block_network: bool = False,
        cidr_allowlist: typing.Optional[collections.abc.Sequence[str]] = None,
        volumes: dict[
            typing.Union[str, os.PathLike], typing.Union[modal.volume.Volume, modal.cloud_bucket_mount.CloudBucketMount]
        ] = {},
        pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
        encrypted_ports: collections.abc.Sequence[int] = [],
        h2_ports: collections.abc.Sequence[int] = [],
        unencrypted_ports: collections.abc.Sequence[int] = [],
        proxy: typing.Optional[modal.proxy.Proxy] = None,
        _experimental_scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
        enable_snapshot: bool = False,
        verbose: bool = False,
    ) -> Sandbox:
        """mdmd:hidden"""
        ...

    class __create_spec(typing_extensions.Protocol):
        def __call__(
            self,
            /,
            *entrypoint_args: str,
            app: typing.Optional[modal.app.App] = None,
            environment_name: typing.Optional[str] = None,
            image: typing.Optional[modal.image.Image] = None,
            secrets: collections.abc.Sequence[modal.secret.Secret] = (),
            network_file_systems: dict[
                typing.Union[str, os.PathLike], modal.network_file_system.NetworkFileSystem
            ] = {},
            timeout: typing.Optional[int] = None,
            workdir: typing.Optional[str] = None,
            gpu: typing.Union[None, str, modal.gpu._GPUConfig] = None,
            cloud: typing.Optional[str] = None,
            region: typing.Union[str, collections.abc.Sequence[str], None] = None,
            cpu: typing.Union[float, tuple[float, float], None] = None,
            memory: typing.Union[int, tuple[int, int], None] = None,
            block_network: bool = False,
            cidr_allowlist: typing.Optional[collections.abc.Sequence[str]] = None,
            volumes: dict[
                typing.Union[str, os.PathLike],
                typing.Union[modal.volume.Volume, modal.cloud_bucket_mount.CloudBucketMount],
            ] = {},
            pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
            encrypted_ports: collections.abc.Sequence[int] = [],
            h2_ports: collections.abc.Sequence[int] = [],
            unencrypted_ports: collections.abc.Sequence[int] = [],
            proxy: typing.Optional[modal.proxy.Proxy] = None,
            verbose: bool = False,
            _experimental_enable_snapshot: bool = False,
            _experimental_scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
            client: typing.Optional[modal.client.Client] = None,
        ) -> Sandbox:
            """Create a new Sandbox to run untrusted, arbitrary code. The Sandbox's corresponding container
            will be created asynchronously.

            **Usage**

            ```python
            app = modal.App.lookup('sandbox-hello-world', create_if_missing=True)
            sandbox = modal.Sandbox.create("echo", "hello world", app=app)
            print(sandbox.stdout.read())
            sandbox.wait()
            ```
            """
            ...

        async def aio(
            self,
            /,
            *entrypoint_args: str,
            app: typing.Optional[modal.app.App] = None,
            environment_name: typing.Optional[str] = None,
            image: typing.Optional[modal.image.Image] = None,
            secrets: collections.abc.Sequence[modal.secret.Secret] = (),
            network_file_systems: dict[
                typing.Union[str, os.PathLike], modal.network_file_system.NetworkFileSystem
            ] = {},
            timeout: typing.Optional[int] = None,
            workdir: typing.Optional[str] = None,
            gpu: typing.Union[None, str, modal.gpu._GPUConfig] = None,
            cloud: typing.Optional[str] = None,
            region: typing.Union[str, collections.abc.Sequence[str], None] = None,
            cpu: typing.Union[float, tuple[float, float], None] = None,
            memory: typing.Union[int, tuple[int, int], None] = None,
            block_network: bool = False,
            cidr_allowlist: typing.Optional[collections.abc.Sequence[str]] = None,
            volumes: dict[
                typing.Union[str, os.PathLike],
                typing.Union[modal.volume.Volume, modal.cloud_bucket_mount.CloudBucketMount],
            ] = {},
            pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
            encrypted_ports: collections.abc.Sequence[int] = [],
            h2_ports: collections.abc.Sequence[int] = [],
            unencrypted_ports: collections.abc.Sequence[int] = [],
            proxy: typing.Optional[modal.proxy.Proxy] = None,
            verbose: bool = False,
            _experimental_enable_snapshot: bool = False,
            _experimental_scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
            client: typing.Optional[modal.client.Client] = None,
        ) -> Sandbox:
            """Create a new Sandbox to run untrusted, arbitrary code. The Sandbox's corresponding container
            will be created asynchronously.

            **Usage**

            ```python
            app = modal.App.lookup('sandbox-hello-world', create_if_missing=True)
            sandbox = modal.Sandbox.create("echo", "hello world", app=app)
            print(sandbox.stdout.read())
            sandbox.wait()
            ```
            """
            ...

    create: __create_spec

    class ___create_spec(typing_extensions.Protocol):
        def __call__(
            self,
            /,
            *entrypoint_args: str,
            app: typing.Optional[modal.app.App] = None,
            environment_name: typing.Optional[str] = None,
            image: typing.Optional[modal.image.Image] = None,
            secrets: collections.abc.Sequence[modal.secret.Secret] = (),
            mounts: collections.abc.Sequence[modal.mount.Mount] = (),
            network_file_systems: dict[
                typing.Union[str, os.PathLike], modal.network_file_system.NetworkFileSystem
            ] = {},
            timeout: typing.Optional[int] = None,
            workdir: typing.Optional[str] = None,
            gpu: typing.Union[None, str, modal.gpu._GPUConfig] = None,
            cloud: typing.Optional[str] = None,
            region: typing.Union[str, collections.abc.Sequence[str], None] = None,
            cpu: typing.Union[float, tuple[float, float], None] = None,
            memory: typing.Union[int, tuple[int, int], None] = None,
            block_network: bool = False,
            cidr_allowlist: typing.Optional[collections.abc.Sequence[str]] = None,
            volumes: dict[
                typing.Union[str, os.PathLike],
                typing.Union[modal.volume.Volume, modal.cloud_bucket_mount.CloudBucketMount],
            ] = {},
            pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
            encrypted_ports: collections.abc.Sequence[int] = [],
            h2_ports: collections.abc.Sequence[int] = [],
            unencrypted_ports: collections.abc.Sequence[int] = [],
            proxy: typing.Optional[modal.proxy.Proxy] = None,
            _experimental_enable_snapshot: bool = False,
            _experimental_scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
            client: typing.Optional[modal.client.Client] = None,
            verbose: bool = False,
        ): ...
        async def aio(
            self,
            /,
            *entrypoint_args: str,
            app: typing.Optional[modal.app.App] = None,
            environment_name: typing.Optional[str] = None,
            image: typing.Optional[modal.image.Image] = None,
            secrets: collections.abc.Sequence[modal.secret.Secret] = (),
            mounts: collections.abc.Sequence[modal.mount.Mount] = (),
            network_file_systems: dict[
                typing.Union[str, os.PathLike], modal.network_file_system.NetworkFileSystem
            ] = {},
            timeout: typing.Optional[int] = None,
            workdir: typing.Optional[str] = None,
            gpu: typing.Union[None, str, modal.gpu._GPUConfig] = None,
            cloud: typing.Optional[str] = None,
            region: typing.Union[str, collections.abc.Sequence[str], None] = None,
            cpu: typing.Union[float, tuple[float, float], None] = None,
            memory: typing.Union[int, tuple[int, int], None] = None,
            block_network: bool = False,
            cidr_allowlist: typing.Optional[collections.abc.Sequence[str]] = None,
            volumes: dict[
                typing.Union[str, os.PathLike],
                typing.Union[modal.volume.Volume, modal.cloud_bucket_mount.CloudBucketMount],
            ] = {},
            pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
            encrypted_ports: collections.abc.Sequence[int] = [],
            h2_ports: collections.abc.Sequence[int] = [],
            unencrypted_ports: collections.abc.Sequence[int] = [],
            proxy: typing.Optional[modal.proxy.Proxy] = None,
            _experimental_enable_snapshot: bool = False,
            _experimental_scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
            client: typing.Optional[modal.client.Client] = None,
            verbose: bool = False,
        ): ...

    _create: ___create_spec

    def _hydrate_metadata(self, handle_metadata: typing.Optional[google.protobuf.message.Message]): ...

    class __from_id_spec(typing_extensions.Protocol):
        def __call__(self, /, sandbox_id: str, client: typing.Optional[modal.client.Client] = None) -> Sandbox:
            """Construct a Sandbox from an id and look up the Sandbox result.

            The ID of a Sandbox object can be accessed using `.object_id`.
            """
            ...

        async def aio(self, /, sandbox_id: str, client: typing.Optional[modal.client.Client] = None) -> Sandbox:
            """Construct a Sandbox from an id and look up the Sandbox result.

            The ID of a Sandbox object can be accessed using `.object_id`.
            """
            ...

    from_id: __from_id_spec

    class __set_tags_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /, tags: dict[str, str], *, client: typing.Optional[modal.client.Client] = None):
            """Set tags (key-value pairs) on the Sandbox. Tags can be used to filter results in `Sandbox.list`."""
            ...

        async def aio(self, /, tags: dict[str, str], *, client: typing.Optional[modal.client.Client] = None):
            """Set tags (key-value pairs) on the Sandbox. Tags can be used to filter results in `Sandbox.list`."""
            ...

    set_tags: __set_tags_spec[typing_extensions.Self]

    class __snapshot_filesystem_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /, timeout: int = 55) -> modal.image.Image:
            """Snapshot the filesystem of the Sandbox.

            Returns an [`Image`](https://modal.com/docs/reference/modal.Image) object which
            can be used to spawn a new Sandbox with the same filesystem.
            """
            ...

        async def aio(self, /, timeout: int = 55) -> modal.image.Image:
            """Snapshot the filesystem of the Sandbox.

            Returns an [`Image`](https://modal.com/docs/reference/modal.Image) object which
            can be used to spawn a new Sandbox with the same filesystem.
            """
            ...

    snapshot_filesystem: __snapshot_filesystem_spec[typing_extensions.Self]

    class __wait_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /, raise_on_termination: bool = True):
            """Wait for the Sandbox to finish running."""
            ...

        async def aio(self, /, raise_on_termination: bool = True):
            """Wait for the Sandbox to finish running."""
            ...

    wait: __wait_spec[typing_extensions.Self]

    class __tunnels_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /, timeout: int = 50) -> dict[int, modal._tunnel.Tunnel]:
            """Get Tunnel metadata for the sandbox.

            Raises `SandboxTimeoutError` if the tunnels are not available after the timeout.

            Returns a dictionary of `Tunnel` objects which are keyed by the container port.

            NOTE: Previous to client [v0.64.153](https://modal.com/docs/reference/changelog#064153-2024-09-30), this
            returned a list of `TunnelData` objects.
            """
            ...

        async def aio(self, /, timeout: int = 50) -> dict[int, modal._tunnel.Tunnel]:
            """Get Tunnel metadata for the sandbox.

            Raises `SandboxTimeoutError` if the tunnels are not available after the timeout.

            Returns a dictionary of `Tunnel` objects which are keyed by the container port.

            NOTE: Previous to client [v0.64.153](https://modal.com/docs/reference/changelog#064153-2024-09-30), this
            returned a list of `TunnelData` objects.
            """
            ...

    tunnels: __tunnels_spec[typing_extensions.Self]

    class __terminate_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /) -> None:
            """Terminate Sandbox execution.

            This is a no-op if the Sandbox has already finished running.
            """
            ...

        async def aio(self, /) -> None:
            """Terminate Sandbox execution.

            This is a no-op if the Sandbox has already finished running.
            """
            ...

    terminate: __terminate_spec[typing_extensions.Self]

    class __poll_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /) -> typing.Optional[int]:
            """Check if the Sandbox has finished running.

            Returns `None` if the Sandbox is still running, else returns the exit code.
            """
            ...

        async def aio(self, /) -> typing.Optional[int]:
            """Check if the Sandbox has finished running.

            Returns `None` if the Sandbox is still running, else returns the exit code.
            """
            ...

    poll: __poll_spec[typing_extensions.Self]

    class ___get_task_id_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /) -> str: ...
        async def aio(self, /) -> str: ...

    _get_task_id: ___get_task_id_spec[typing_extensions.Self]

    class __exec_spec(typing_extensions.Protocol[SUPERSELF]):
        @typing.overload
        def __call__(
            self,
            /,
            *cmds: str,
            pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
            stdout: modal.stream_type.StreamType = modal.stream_type.StreamType.PIPE,
            stderr: modal.stream_type.StreamType = modal.stream_type.StreamType.PIPE,
            timeout: typing.Optional[int] = None,
            workdir: typing.Optional[str] = None,
            secrets: collections.abc.Sequence[modal.secret.Secret] = (),
            text: typing.Literal[True] = True,
            bufsize: typing.Literal[-1, 1] = -1,
            _pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
        ) -> modal.container_process.ContainerProcess[str]: ...
        @typing.overload
        def __call__(
            self,
            /,
            *cmds: str,
            pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
            stdout: modal.stream_type.StreamType = modal.stream_type.StreamType.PIPE,
            stderr: modal.stream_type.StreamType = modal.stream_type.StreamType.PIPE,
            timeout: typing.Optional[int] = None,
            workdir: typing.Optional[str] = None,
            secrets: collections.abc.Sequence[modal.secret.Secret] = (),
            text: typing.Literal[False] = False,
            bufsize: typing.Literal[-1, 1] = -1,
            _pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
        ) -> modal.container_process.ContainerProcess[bytes]: ...
        @typing.overload
        async def aio(
            self,
            /,
            *cmds: str,
            pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
            stdout: modal.stream_type.StreamType = modal.stream_type.StreamType.PIPE,
            stderr: modal.stream_type.StreamType = modal.stream_type.StreamType.PIPE,
            timeout: typing.Optional[int] = None,
            workdir: typing.Optional[str] = None,
            secrets: collections.abc.Sequence[modal.secret.Secret] = (),
            text: typing.Literal[True] = True,
            bufsize: typing.Literal[-1, 1] = -1,
            _pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
        ) -> modal.container_process.ContainerProcess[str]: ...
        @typing.overload
        async def aio(
            self,
            /,
            *cmds: str,
            pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
            stdout: modal.stream_type.StreamType = modal.stream_type.StreamType.PIPE,
            stderr: modal.stream_type.StreamType = modal.stream_type.StreamType.PIPE,
            timeout: typing.Optional[int] = None,
            workdir: typing.Optional[str] = None,
            secrets: collections.abc.Sequence[modal.secret.Secret] = (),
            text: typing.Literal[False] = False,
            bufsize: typing.Literal[-1, 1] = -1,
            _pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
        ) -> modal.container_process.ContainerProcess[bytes]: ...

    exec: __exec_spec[typing_extensions.Self]

    class ___experimental_snapshot_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /) -> modal.snapshot.SandboxSnapshot: ...
        async def aio(self, /) -> modal.snapshot.SandboxSnapshot: ...

    _experimental_snapshot: ___experimental_snapshot_spec[typing_extensions.Self]

    class ___experimental_from_snapshot_spec(typing_extensions.Protocol):
        def __call__(
            self, /, snapshot: modal.snapshot.SandboxSnapshot, client: typing.Optional[modal.client.Client] = None
        ): ...
        async def aio(
            self, /, snapshot: modal.snapshot.SandboxSnapshot, client: typing.Optional[modal.client.Client] = None
        ): ...

    _experimental_from_snapshot: ___experimental_from_snapshot_spec

    class __open_spec(typing_extensions.Protocol[SUPERSELF]):
        @typing.overload
        def __call__(self, /, path: str, mode: _typeshed.OpenTextMode) -> modal.file_io.FileIO[str]: ...
        @typing.overload
        def __call__(self, /, path: str, mode: _typeshed.OpenBinaryMode) -> modal.file_io.FileIO[bytes]: ...
        @typing.overload
        async def aio(self, /, path: str, mode: _typeshed.OpenTextMode) -> modal.file_io.FileIO[str]: ...
        @typing.overload
        async def aio(self, /, path: str, mode: _typeshed.OpenBinaryMode) -> modal.file_io.FileIO[bytes]: ...

    open: __open_spec[typing_extensions.Self]

    class __ls_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /, path: str) -> list[str]:
            """List the contents of a directory in the Sandbox."""
            ...

        async def aio(self, /, path: str) -> list[str]:
            """List the contents of a directory in the Sandbox."""
            ...

    ls: __ls_spec[typing_extensions.Self]

    class __mkdir_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /, path: str, parents: bool = False) -> None:
            """Create a new directory in the Sandbox."""
            ...

        async def aio(self, /, path: str, parents: bool = False) -> None:
            """Create a new directory in the Sandbox."""
            ...

    mkdir: __mkdir_spec[typing_extensions.Self]

    class __rm_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /, path: str, recursive: bool = False) -> None:
            """Remove a file or directory in the Sandbox."""
            ...

        async def aio(self, /, path: str, recursive: bool = False) -> None:
            """Remove a file or directory in the Sandbox."""
            ...

    rm: __rm_spec[typing_extensions.Self]

    class __watch_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(
            self,
            /,
            path: str,
            filter: typing.Optional[list[modal.file_io.FileWatchEventType]] = None,
            recursive: typing.Optional[bool] = None,
            timeout: typing.Optional[int] = None,
        ) -> typing.Iterator[modal.file_io.FileWatchEvent]:
            """Watch a file or directory in the Sandbox for changes."""
            ...

        def aio(
            self,
            /,
            path: str,
            filter: typing.Optional[list[modal.file_io.FileWatchEventType]] = None,
            recursive: typing.Optional[bool] = None,
            timeout: typing.Optional[int] = None,
        ) -> typing.AsyncIterator[modal.file_io.FileWatchEvent]:
            """Watch a file or directory in the Sandbox for changes."""
            ...

    watch: __watch_spec[typing_extensions.Self]

    @property
    def stdout(self) -> modal.io_streams.StreamReader[str]:
        """[`StreamReader`](https://modal.com/docs/reference/modal.io_streams#modalio_streamsstreamreader) for
        the sandbox's stdout stream.
        """
        ...

    @property
    def stderr(self) -> modal.io_streams.StreamReader[str]:
        """[`StreamReader`](https://modal.com/docs/reference/modal.io_streams#modalio_streamsstreamreader) for
        the Sandbox's stderr stream.
        """
        ...

    @property
    def stdin(self) -> modal.io_streams.StreamWriter:
        """[`StreamWriter`](https://modal.com/docs/reference/modal.io_streams#modalio_streamsstreamwriter) for
        the Sandbox's stdin stream.
        """
        ...

    @property
    def returncode(self) -> typing.Optional[int]:
        """Return code of the Sandbox process if it has finished running, else `None`."""
        ...

    class __list_spec(typing_extensions.Protocol):
        def __call__(
            self,
            /,
            *,
            app_id: typing.Optional[str] = None,
            tags: typing.Optional[dict[str, str]] = None,
            client: typing.Optional[modal.client.Client] = None,
        ) -> typing.Generator[Sandbox, None, None]:
            """List all Sandboxes for the current Environment or App ID (if specified). If tags are specified, only
            Sandboxes that have at least those tags are returned. Returns an iterator over `Sandbox` objects.
            """
            ...

        def aio(
            self,
            /,
            *,
            app_id: typing.Optional[str] = None,
            tags: typing.Optional[dict[str, str]] = None,
            client: typing.Optional[modal.client.Client] = None,
        ) -> collections.abc.AsyncGenerator[Sandbox, None]:
            """List all Sandboxes for the current Environment or App ID (if specified). If tags are specified, only
            Sandboxes that have at least those tags are returned. Returns an iterator over `Sandbox` objects.
            """
            ...

    list: __list_spec

_default_image: modal.image._Image
