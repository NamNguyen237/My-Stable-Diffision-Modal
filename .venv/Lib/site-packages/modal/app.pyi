import collections.abc
import modal._functions
import modal._partial_function
import modal._utils.function_utils
import modal.client
import modal.cloud_bucket_mount
import modal.cls
import modal.functions
import modal.gpu
import modal.image
import modal.network_file_system
import modal.partial_function
import modal.proxy
import modal.retries
import modal.running_app
import modal.schedule
import modal.scheduler_placement
import modal.secret
import modal.volume
import pathlib
import synchronicity.combined_types
import typing
import typing_extensions

class _LocalEntrypoint:
    _info: modal._utils.function_utils.FunctionInfo
    _app: _App

    def __init__(self, info: modal._utils.function_utils.FunctionInfo, app: _App) -> None:
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        """Call self as a function."""
        ...

    @property
    def info(self) -> modal._utils.function_utils.FunctionInfo: ...
    @property
    def app(self) -> _App: ...

class LocalEntrypoint:
    _info: modal._utils.function_utils.FunctionInfo
    _app: App

    def __init__(self, info: modal._utils.function_utils.FunctionInfo, app: App) -> None: ...
    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any: ...
    @property
    def info(self) -> modal._utils.function_utils.FunctionInfo: ...
    @property
    def app(self) -> App: ...

def check_sequence(items: typing.Sequence[typing.Any], item_type: type[typing.Any], error_msg: str) -> None: ...

CLS_T = typing.TypeVar("CLS_T", bound="type[typing.Any]")

P = typing_extensions.ParamSpec("P")

ReturnType = typing.TypeVar("ReturnType")

OriginalReturnType = typing.TypeVar("OriginalReturnType")

class _FunctionDecoratorType:
    @typing.overload
    def __call__(
        self, func: modal.partial_function.PartialFunction[P, ReturnType, OriginalReturnType]
    ) -> modal.functions.Function[P, ReturnType, OriginalReturnType]: ...
    @typing.overload
    def __call__(
        self, func: collections.abc.Callable[P, collections.abc.Coroutine[typing.Any, typing.Any, ReturnType]]
    ) -> modal.functions.Function[P, ReturnType, collections.abc.Coroutine[typing.Any, typing.Any, ReturnType]]: ...
    @typing.overload
    def __call__(
        self, func: collections.abc.Callable[P, ReturnType]
    ) -> modal.functions.Function[P, ReturnType, ReturnType]: ...

class _App:
    """A Modal App is a group of functions and classes that are deployed together.

    The app serves at least three purposes:

    * A unit of deployment for functions and classes.
    * Syncing of identities of (primarily) functions and classes across processes
      (your local Python interpreter and every Modal container active in your application).
    * Manage log collection for everything that happens inside your code.

    **Registering functions with an app**

    The most common way to explicitly register an Object with an app is through the
    `@app.function()` decorator. It both registers the annotated function itself and
    other passed objects, like schedules and secrets, with the app:

    ```python
    import modal

    app = modal.App()

    @app.function(
        secrets=[modal.Secret.from_name("some_secret")],
        schedule=modal.Period(days=1),
    )
    def foo():
        pass
    ```

    In this example, the secret and schedule are registered with the app.
    """

    _all_apps: typing.ClassVar[dict[typing.Optional[str], list[_App]]]
    _container_app: typing.ClassVar[typing.Optional[_App]]
    _name: typing.Optional[str]
    _description: typing.Optional[str]
    _functions: dict[str, modal._functions._Function]
    _classes: dict[str, modal.cls._Cls]
    _image: typing.Optional[modal.image._Image]
    _secrets: collections.abc.Sequence[modal.secret._Secret]
    _volumes: dict[typing.Union[str, pathlib.PurePosixPath], modal.volume._Volume]
    _web_endpoints: list[str]
    _local_entrypoints: dict[str, _LocalEntrypoint]
    _app_id: typing.Optional[str]
    _running_app: typing.Optional[modal.running_app.RunningApp]
    _client: typing.Optional[modal.client._Client]
    _include_source_default: typing.Optional[bool]

    def __init__(
        self,
        name: typing.Optional[str] = None,
        *,
        image: typing.Optional[modal.image._Image] = None,
        secrets: collections.abc.Sequence[modal.secret._Secret] = [],
        volumes: dict[typing.Union[str, pathlib.PurePosixPath], modal.volume._Volume] = {},
        include_source: typing.Optional[bool] = None,
    ) -> None:
        """Construct a new app, optionally with default image, mounts, secrets, or volumes.

        ```python notest
        image = modal.Image.debian_slim().pip_install(...)
        secret = modal.Secret.from_name("my-secret")
        volume = modal.Volume.from_name("my-data")
        app = modal.App(image=image, secrets=[secret], volumes={"/mnt/data": volume})
        ```
        """
        ...

    @property
    def name(self) -> typing.Optional[str]:
        """The user-provided name of the App."""
        ...

    @property
    def is_interactive(self) -> bool:
        """Whether the current app for the app is running in interactive mode."""
        ...

    @property
    def app_id(self) -> typing.Optional[str]:
        """Return the app_id of a running or stopped app."""
        ...

    @property
    def description(self) -> typing.Optional[str]:
        """The App's `name`, if available, or a fallback descriptive identifier."""
        ...

    @staticmethod
    async def lookup(
        name: str,
        *,
        client: typing.Optional[modal.client._Client] = None,
        environment_name: typing.Optional[str] = None,
        create_if_missing: bool = False,
    ) -> _App:
        """Look up an App with a given name, creating a new App if necessary.

        Note that Apps created through this method will be in a deployed state,
        but they will not have any associated Functions or Classes. This method
        is mainly useful for creating an App to associate with a Sandbox:

        ```python
        app = modal.App.lookup("my-app", create_if_missing=True)
        modal.Sandbox.create("echo", "hi", app=app)
        ```
        """
        ...

    def set_description(self, description: str): ...
    def _validate_blueprint_value(self, key: str, value: typing.Any): ...
    @property
    def image(self) -> modal.image._Image: ...
    @image.setter
    def image(self, value): ...
    def _uncreate_all_objects(self): ...
    def _set_local_app(
        self, client: modal.client._Client, running_app: modal.running_app.RunningApp
    ) -> typing.AsyncContextManager[None]: ...
    def run(
        self,
        *,
        client: typing.Optional[modal.client._Client] = None,
        detach: bool = False,
        interactive: bool = False,
        environment_name: typing.Optional[str] = None,
    ) -> typing.AsyncContextManager[_App]:
        """Context manager that runs an ephemeral app on Modal.

        Use this as the main entry point for your Modal application. All calls
        to Modal Functions should be made within the scope of this context
        manager, and they will correspond to the current App.

        **Example**

        ```python notest
        with app.run():
            some_modal_function.remote()
        ```

        To enable output printing (i.e., to see App logs), use `modal.enable_output()`:

        ```python notest
        with modal.enable_output():
            with app.run():
                some_modal_function.remote()
        ```

        Note that you should not invoke this in global scope of a file where you have
        Modal Functions or Classes defined, since that would run the block when the Function
        or Cls is imported in your containers as well. If you want to run it as your entrypoint,
        consider protecting it:

        ```python
        if __name__ == "__main__":
            with app.run():
                some_modal_function.remote()
        ```

        You can then run your script with:

        ```shell
        python app_module.py
        ```
        """
        ...

    async def deploy(
        self,
        *,
        name: typing.Optional[str] = None,
        environment_name: typing.Optional[str] = None,
        tag: str = "",
        client: typing.Optional[modal.client._Client] = None,
    ) -> typing_extensions.Self:
        """Deploy the App so that it is available persistently.

        Deployed Apps will be avaible for lookup or web-based invocations until they are stopped.
        Unlike with `App.run`, this method will return as soon as the deployment completes.

        This method is a programmatic alternative to the `modal deploy` CLI command.

        Examples:

        ```python notest
        app = App("my-app")
        app.deploy()
        ```

        To enable output printing (i.e., to see build logs), use `modal.enable_output()`:

        ```python notest
        app = App("my-app")
        with modal.enable_output():
            app.deploy()
        ```

        Unlike with `App.run`, Function logs will not stream back to the local client after the
        App is deployed.

        Note that you should not invoke this method in global scope, as that would redeploy
        the App every time the file is imported. If you want to write a programmatic deployment
        script, protect this call so that it only runs when the file is executed directly:

        ```python notest
        if __name__ == "__main__":
            with modal.enable_output():
                app.deploy()
        ```

        Then you can deploy your app with:

        ```shell
        python app_module.py
        ```
        """
        ...

    def _get_default_image(self): ...
    def _get_watch_mounts(self): ...
    def _add_function(self, function: modal._functions._Function, is_web_endpoint: bool): ...
    def _add_class(self, tag: str, cls: modal.cls._Cls): ...
    def _init_container(self, client: modal.client._Client, running_app: modal.running_app.RunningApp): ...
    @property
    def registered_functions(self) -> dict[str, modal._functions._Function]:
        """All modal.Function objects registered on the app."""
        ...

    @property
    def registered_classes(self) -> dict[str, modal.cls._Cls]:
        """All modal.Cls objects registered on the app."""
        ...

    @property
    def registered_entrypoints(self) -> dict[str, _LocalEntrypoint]:
        """All local CLI entrypoints registered on the app."""
        ...

    @property
    def registered_web_endpoints(self) -> list[str]:
        """Names of web endpoint (ie. webhook) functions registered on the app."""
        ...

    def local_entrypoint(
        self, _warn_parentheses_missing: typing.Any = None, *, name: typing.Optional[str] = None
    ) -> collections.abc.Callable[[collections.abc.Callable[..., typing.Any]], _LocalEntrypoint]:
        """Decorate a function to be used as a CLI entrypoint for a Modal App.

        These functions can be used to define code that runs locally to set up the app,
        and act as an entrypoint to start Modal functions from. Note that regular
        Modal functions can also be used as CLI entrypoints, but unlike `local_entrypoint`,
        those functions are executed remotely directly.

        **Example**

        ```python
        @app.local_entrypoint()
        def main():
            some_modal_function.remote()
        ```

        You can call the function using `modal run` directly from the CLI:

        ```shell
        modal run app_module.py
        ```

        Note that an explicit [`app.run()`](https://modal.com/docs/reference/modal.App#run) is not needed, as an
        [app](https://modal.com/docs/guide/apps) is automatically created for you.

        **Multiple Entrypoints**

        If you have multiple `local_entrypoint` functions, you can qualify the name of your app and function:

        ```shell
        modal run app_module.py::app.some_other_function
        ```

        **Parsing Arguments**

        If your entrypoint function take arguments with primitive types, `modal run` automatically parses them as
        CLI options.
        For example, the following function can be called with `modal run app_module.py --foo 1 --bar "hello"`:

        ```python
        @app.local_entrypoint()
        def main(foo: int, bar: str):
            some_modal_function.call(foo, bar)
        ```

        Currently, `str`, `int`, `float`, `bool`, and `datetime.datetime` are supported.
        Use `modal run app_module.py --help` for more information on usage.
        """
        ...

    def function(
        self,
        _warn_parentheses_missing: typing.Any = None,
        *,
        image: typing.Optional[modal.image._Image] = None,
        schedule: typing.Optional[modal.schedule.Schedule] = None,
        secrets: collections.abc.Sequence[modal.secret._Secret] = (),
        gpu: typing.Union[None, str, modal.gpu._GPUConfig, list[typing.Union[None, str, modal.gpu._GPUConfig]]] = None,
        serialized: bool = False,
        network_file_systems: dict[
            typing.Union[str, pathlib.PurePosixPath], modal.network_file_system._NetworkFileSystem
        ] = {},
        volumes: dict[
            typing.Union[str, pathlib.PurePosixPath],
            typing.Union[modal.volume._Volume, modal.cloud_bucket_mount._CloudBucketMount],
        ] = {},
        cpu: typing.Union[float, tuple[float, float], None] = None,
        memory: typing.Union[int, tuple[int, int], None] = None,
        ephemeral_disk: typing.Optional[int] = None,
        min_containers: typing.Optional[int] = None,
        max_containers: typing.Optional[int] = None,
        buffer_containers: typing.Optional[int] = None,
        scaledown_window: typing.Optional[int] = None,
        proxy: typing.Optional[modal.proxy._Proxy] = None,
        retries: typing.Union[int, modal.retries.Retries, None] = None,
        timeout: typing.Optional[int] = None,
        name: typing.Optional[str] = None,
        is_generator: typing.Optional[bool] = None,
        cloud: typing.Optional[str] = None,
        region: typing.Union[str, collections.abc.Sequence[str], None] = None,
        enable_memory_snapshot: bool = False,
        block_network: bool = False,
        restrict_modal_access: bool = False,
        max_inputs: typing.Optional[int] = None,
        i6pn: typing.Optional[bool] = None,
        include_source: typing.Optional[bool] = None,
        experimental_options: typing.Optional[dict[str, typing.Any]] = None,
        _experimental_scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
        _experimental_proxy_ip: typing.Optional[str] = None,
        _experimental_custom_scaling_factor: typing.Optional[float] = None,
        _experimental_enable_gpu_snapshot: bool = False,
        keep_warm: typing.Optional[int] = None,
        concurrency_limit: typing.Optional[int] = None,
        container_idle_timeout: typing.Optional[int] = None,
        allow_concurrent_inputs: typing.Optional[int] = None,
        _experimental_buffer_containers: typing.Optional[int] = None,
        allow_cross_region_volumes: typing.Optional[bool] = None,
    ) -> _FunctionDecoratorType:
        """Decorator to register a new Modal Function with this App."""
        ...

    @typing_extensions.dataclass_transform(
        field_specifiers=(modal.cls.parameter,),
        kw_only_default=True,
    )
    def cls(
        self,
        _warn_parentheses_missing: typing.Optional[bool] = None,
        *,
        image: typing.Optional[modal.image._Image] = None,
        secrets: collections.abc.Sequence[modal.secret._Secret] = (),
        gpu: typing.Union[None, str, modal.gpu._GPUConfig, list[typing.Union[None, str, modal.gpu._GPUConfig]]] = None,
        serialized: bool = False,
        network_file_systems: dict[
            typing.Union[str, pathlib.PurePosixPath], modal.network_file_system._NetworkFileSystem
        ] = {},
        volumes: dict[
            typing.Union[str, pathlib.PurePosixPath],
            typing.Union[modal.volume._Volume, modal.cloud_bucket_mount._CloudBucketMount],
        ] = {},
        cpu: typing.Union[float, tuple[float, float], None] = None,
        memory: typing.Union[int, tuple[int, int], None] = None,
        ephemeral_disk: typing.Optional[int] = None,
        min_containers: typing.Optional[int] = None,
        max_containers: typing.Optional[int] = None,
        buffer_containers: typing.Optional[int] = None,
        scaledown_window: typing.Optional[int] = None,
        proxy: typing.Optional[modal.proxy._Proxy] = None,
        retries: typing.Union[int, modal.retries.Retries, None] = None,
        timeout: typing.Optional[int] = None,
        cloud: typing.Optional[str] = None,
        region: typing.Union[str, collections.abc.Sequence[str], None] = None,
        enable_memory_snapshot: bool = False,
        block_network: bool = False,
        restrict_modal_access: bool = False,
        max_inputs: typing.Optional[int] = None,
        include_source: typing.Optional[bool] = None,
        experimental_options: typing.Optional[dict[str, typing.Any]] = None,
        _experimental_scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
        _experimental_proxy_ip: typing.Optional[str] = None,
        _experimental_custom_scaling_factor: typing.Optional[float] = None,
        _experimental_enable_gpu_snapshot: bool = False,
        keep_warm: typing.Optional[int] = None,
        concurrency_limit: typing.Optional[int] = None,
        container_idle_timeout: typing.Optional[int] = None,
        allow_concurrent_inputs: typing.Optional[int] = None,
        _experimental_buffer_containers: typing.Optional[int] = None,
        allow_cross_region_volumes: typing.Optional[bool] = None,
    ) -> collections.abc.Callable[[typing.Union[CLS_T, modal._partial_function._PartialFunction]], CLS_T]:
        """Decorator to register a new Modal [Cls](https://modal.com/docs/reference/modal.Cls) with this App."""
        ...

    def include(self, /, other_app: _App) -> typing_extensions.Self:
        """Include another App's objects in this one.

        Useful for splitting up Modal Apps across different self-contained files.

        ```python
        app_a = modal.App("a")
        @app.function()
        def foo():
            ...

        app_b = modal.App("b")
        @app.function()
        def bar():
            ...

        app_a.include(app_b)

        @app_a.local_entrypoint()
        def main():
            # use function declared on the included app
            bar.remote()
        ```
        """
        ...

    def _logs(self, client: typing.Optional[modal.client._Client] = None) -> collections.abc.AsyncGenerator[str, None]:
        """Stream logs from the app.

        This method is considered private and its interface may change - use at your own risk!
        """
        ...

    @classmethod
    def _get_container_app(cls) -> typing.Optional[_App]:
        """Returns the `App` running inside a container.

        This will return `None` outside of a Modal container.
        """
        ...

    @classmethod
    def _reset_container_app(cls):
        """Only used for tests."""
        ...

SUPERSELF = typing.TypeVar("SUPERSELF", covariant=True)

class App:
    """A Modal App is a group of functions and classes that are deployed together.

    The app serves at least three purposes:

    * A unit of deployment for functions and classes.
    * Syncing of identities of (primarily) functions and classes across processes
      (your local Python interpreter and every Modal container active in your application).
    * Manage log collection for everything that happens inside your code.

    **Registering functions with an app**

    The most common way to explicitly register an Object with an app is through the
    `@app.function()` decorator. It both registers the annotated function itself and
    other passed objects, like schedules and secrets, with the app:

    ```python
    import modal

    app = modal.App()

    @app.function(
        secrets=[modal.Secret.from_name("some_secret")],
        schedule=modal.Period(days=1),
    )
    def foo():
        pass
    ```

    In this example, the secret and schedule are registered with the app.
    """

    _all_apps: typing.ClassVar[dict[typing.Optional[str], list[App]]]
    _container_app: typing.ClassVar[typing.Optional[App]]
    _name: typing.Optional[str]
    _description: typing.Optional[str]
    _functions: dict[str, modal.functions.Function]
    _classes: dict[str, modal.cls.Cls]
    _image: typing.Optional[modal.image.Image]
    _secrets: collections.abc.Sequence[modal.secret.Secret]
    _volumes: dict[typing.Union[str, pathlib.PurePosixPath], modal.volume.Volume]
    _web_endpoints: list[str]
    _local_entrypoints: dict[str, LocalEntrypoint]
    _app_id: typing.Optional[str]
    _running_app: typing.Optional[modal.running_app.RunningApp]
    _client: typing.Optional[modal.client.Client]
    _include_source_default: typing.Optional[bool]

    def __init__(
        self,
        name: typing.Optional[str] = None,
        *,
        image: typing.Optional[modal.image.Image] = None,
        secrets: collections.abc.Sequence[modal.secret.Secret] = [],
        volumes: dict[typing.Union[str, pathlib.PurePosixPath], modal.volume.Volume] = {},
        include_source: typing.Optional[bool] = None,
    ) -> None:
        """Construct a new app, optionally with default image, mounts, secrets, or volumes.

        ```python notest
        image = modal.Image.debian_slim().pip_install(...)
        secret = modal.Secret.from_name("my-secret")
        volume = modal.Volume.from_name("my-data")
        app = modal.App(image=image, secrets=[secret], volumes={"/mnt/data": volume})
        ```
        """
        ...

    @property
    def name(self) -> typing.Optional[str]:
        """The user-provided name of the App."""
        ...

    @property
    def is_interactive(self) -> bool:
        """Whether the current app for the app is running in interactive mode."""
        ...

    @property
    def app_id(self) -> typing.Optional[str]:
        """Return the app_id of a running or stopped app."""
        ...

    @property
    def description(self) -> typing.Optional[str]:
        """The App's `name`, if available, or a fallback descriptive identifier."""
        ...

    class __lookup_spec(typing_extensions.Protocol):
        def __call__(
            self,
            /,
            name: str,
            *,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
            create_if_missing: bool = False,
        ) -> App:
            """Look up an App with a given name, creating a new App if necessary.

            Note that Apps created through this method will be in a deployed state,
            but they will not have any associated Functions or Classes. This method
            is mainly useful for creating an App to associate with a Sandbox:

            ```python
            app = modal.App.lookup("my-app", create_if_missing=True)
            modal.Sandbox.create("echo", "hi", app=app)
            ```
            """
            ...

        async def aio(
            self,
            /,
            name: str,
            *,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
            create_if_missing: bool = False,
        ) -> App:
            """Look up an App with a given name, creating a new App if necessary.

            Note that Apps created through this method will be in a deployed state,
            but they will not have any associated Functions or Classes. This method
            is mainly useful for creating an App to associate with a Sandbox:

            ```python
            app = modal.App.lookup("my-app", create_if_missing=True)
            modal.Sandbox.create("echo", "hi", app=app)
            ```
            """
            ...

    lookup: __lookup_spec

    def set_description(self, description: str): ...
    def _validate_blueprint_value(self, key: str, value: typing.Any): ...
    @property
    def image(self) -> modal.image.Image: ...
    @image.setter
    def image(self, value): ...
    def _uncreate_all_objects(self): ...

    class ___set_local_app_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(
            self, /, client: modal.client.Client, running_app: modal.running_app.RunningApp
        ) -> synchronicity.combined_types.AsyncAndBlockingContextManager[None]: ...
        def aio(
            self, /, client: modal.client.Client, running_app: modal.running_app.RunningApp
        ) -> typing.AsyncContextManager[None]: ...

    _set_local_app: ___set_local_app_spec[typing_extensions.Self]

    class __run_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(
            self,
            /,
            *,
            client: typing.Optional[modal.client.Client] = None,
            detach: bool = False,
            interactive: bool = False,
            environment_name: typing.Optional[str] = None,
        ) -> synchronicity.combined_types.AsyncAndBlockingContextManager[App]:
            """Context manager that runs an ephemeral app on Modal.

            Use this as the main entry point for your Modal application. All calls
            to Modal Functions should be made within the scope of this context
            manager, and they will correspond to the current App.

            **Example**

            ```python notest
            with app.run():
                some_modal_function.remote()
            ```

            To enable output printing (i.e., to see App logs), use `modal.enable_output()`:

            ```python notest
            with modal.enable_output():
                with app.run():
                    some_modal_function.remote()
            ```

            Note that you should not invoke this in global scope of a file where you have
            Modal Functions or Classes defined, since that would run the block when the Function
            or Cls is imported in your containers as well. If you want to run it as your entrypoint,
            consider protecting it:

            ```python
            if __name__ == "__main__":
                with app.run():
                    some_modal_function.remote()
            ```

            You can then run your script with:

            ```shell
            python app_module.py
            ```
            """
            ...

        def aio(
            self,
            /,
            *,
            client: typing.Optional[modal.client.Client] = None,
            detach: bool = False,
            interactive: bool = False,
            environment_name: typing.Optional[str] = None,
        ) -> typing.AsyncContextManager[App]:
            """Context manager that runs an ephemeral app on Modal.

            Use this as the main entry point for your Modal application. All calls
            to Modal Functions should be made within the scope of this context
            manager, and they will correspond to the current App.

            **Example**

            ```python notest
            with app.run():
                some_modal_function.remote()
            ```

            To enable output printing (i.e., to see App logs), use `modal.enable_output()`:

            ```python notest
            with modal.enable_output():
                with app.run():
                    some_modal_function.remote()
            ```

            Note that you should not invoke this in global scope of a file where you have
            Modal Functions or Classes defined, since that would run the block when the Function
            or Cls is imported in your containers as well. If you want to run it as your entrypoint,
            consider protecting it:

            ```python
            if __name__ == "__main__":
                with app.run():
                    some_modal_function.remote()
            ```

            You can then run your script with:

            ```shell
            python app_module.py
            ```
            """
            ...

    run: __run_spec[typing_extensions.Self]

    class __deploy_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(
            self,
            /,
            *,
            name: typing.Optional[str] = None,
            environment_name: typing.Optional[str] = None,
            tag: str = "",
            client: typing.Optional[modal.client.Client] = None,
        ) -> SUPERSELF:
            """Deploy the App so that it is available persistently.

            Deployed Apps will be avaible for lookup or web-based invocations until they are stopped.
            Unlike with `App.run`, this method will return as soon as the deployment completes.

            This method is a programmatic alternative to the `modal deploy` CLI command.

            Examples:

            ```python notest
            app = App("my-app")
            app.deploy()
            ```

            To enable output printing (i.e., to see build logs), use `modal.enable_output()`:

            ```python notest
            app = App("my-app")
            with modal.enable_output():
                app.deploy()
            ```

            Unlike with `App.run`, Function logs will not stream back to the local client after the
            App is deployed.

            Note that you should not invoke this method in global scope, as that would redeploy
            the App every time the file is imported. If you want to write a programmatic deployment
            script, protect this call so that it only runs when the file is executed directly:

            ```python notest
            if __name__ == "__main__":
                with modal.enable_output():
                    app.deploy()
            ```

            Then you can deploy your app with:

            ```shell
            python app_module.py
            ```
            """
            ...

        async def aio(
            self,
            /,
            *,
            name: typing.Optional[str] = None,
            environment_name: typing.Optional[str] = None,
            tag: str = "",
            client: typing.Optional[modal.client.Client] = None,
        ) -> SUPERSELF:
            """Deploy the App so that it is available persistently.

            Deployed Apps will be avaible for lookup or web-based invocations until they are stopped.
            Unlike with `App.run`, this method will return as soon as the deployment completes.

            This method is a programmatic alternative to the `modal deploy` CLI command.

            Examples:

            ```python notest
            app = App("my-app")
            app.deploy()
            ```

            To enable output printing (i.e., to see build logs), use `modal.enable_output()`:

            ```python notest
            app = App("my-app")
            with modal.enable_output():
                app.deploy()
            ```

            Unlike with `App.run`, Function logs will not stream back to the local client after the
            App is deployed.

            Note that you should not invoke this method in global scope, as that would redeploy
            the App every time the file is imported. If you want to write a programmatic deployment
            script, protect this call so that it only runs when the file is executed directly:

            ```python notest
            if __name__ == "__main__":
                with modal.enable_output():
                    app.deploy()
            ```

            Then you can deploy your app with:

            ```shell
            python app_module.py
            ```
            """
            ...

    deploy: __deploy_spec[typing_extensions.Self]

    def _get_default_image(self): ...
    def _get_watch_mounts(self): ...
    def _add_function(self, function: modal.functions.Function, is_web_endpoint: bool): ...
    def _add_class(self, tag: str, cls: modal.cls.Cls): ...
    def _init_container(self, client: modal.client.Client, running_app: modal.running_app.RunningApp): ...
    @property
    def registered_functions(self) -> dict[str, modal.functions.Function]:
        """All modal.Function objects registered on the app."""
        ...

    @property
    def registered_classes(self) -> dict[str, modal.cls.Cls]:
        """All modal.Cls objects registered on the app."""
        ...

    @property
    def registered_entrypoints(self) -> dict[str, LocalEntrypoint]:
        """All local CLI entrypoints registered on the app."""
        ...

    @property
    def registered_web_endpoints(self) -> list[str]:
        """Names of web endpoint (ie. webhook) functions registered on the app."""
        ...

    def local_entrypoint(
        self, _warn_parentheses_missing: typing.Any = None, *, name: typing.Optional[str] = None
    ) -> collections.abc.Callable[[collections.abc.Callable[..., typing.Any]], LocalEntrypoint]:
        """Decorate a function to be used as a CLI entrypoint for a Modal App.

        These functions can be used to define code that runs locally to set up the app,
        and act as an entrypoint to start Modal functions from. Note that regular
        Modal functions can also be used as CLI entrypoints, but unlike `local_entrypoint`,
        those functions are executed remotely directly.

        **Example**

        ```python
        @app.local_entrypoint()
        def main():
            some_modal_function.remote()
        ```

        You can call the function using `modal run` directly from the CLI:

        ```shell
        modal run app_module.py
        ```

        Note that an explicit [`app.run()`](https://modal.com/docs/reference/modal.App#run) is not needed, as an
        [app](https://modal.com/docs/guide/apps) is automatically created for you.

        **Multiple Entrypoints**

        If you have multiple `local_entrypoint` functions, you can qualify the name of your app and function:

        ```shell
        modal run app_module.py::app.some_other_function
        ```

        **Parsing Arguments**

        If your entrypoint function take arguments with primitive types, `modal run` automatically parses them as
        CLI options.
        For example, the following function can be called with `modal run app_module.py --foo 1 --bar "hello"`:

        ```python
        @app.local_entrypoint()
        def main(foo: int, bar: str):
            some_modal_function.call(foo, bar)
        ```

        Currently, `str`, `int`, `float`, `bool`, and `datetime.datetime` are supported.
        Use `modal run app_module.py --help` for more information on usage.
        """
        ...

    def function(
        self,
        _warn_parentheses_missing: typing.Any = None,
        *,
        image: typing.Optional[modal.image.Image] = None,
        schedule: typing.Optional[modal.schedule.Schedule] = None,
        secrets: collections.abc.Sequence[modal.secret.Secret] = (),
        gpu: typing.Union[None, str, modal.gpu._GPUConfig, list[typing.Union[None, str, modal.gpu._GPUConfig]]] = None,
        serialized: bool = False,
        network_file_systems: dict[
            typing.Union[str, pathlib.PurePosixPath], modal.network_file_system.NetworkFileSystem
        ] = {},
        volumes: dict[
            typing.Union[str, pathlib.PurePosixPath],
            typing.Union[modal.volume.Volume, modal.cloud_bucket_mount.CloudBucketMount],
        ] = {},
        cpu: typing.Union[float, tuple[float, float], None] = None,
        memory: typing.Union[int, tuple[int, int], None] = None,
        ephemeral_disk: typing.Optional[int] = None,
        min_containers: typing.Optional[int] = None,
        max_containers: typing.Optional[int] = None,
        buffer_containers: typing.Optional[int] = None,
        scaledown_window: typing.Optional[int] = None,
        proxy: typing.Optional[modal.proxy.Proxy] = None,
        retries: typing.Union[int, modal.retries.Retries, None] = None,
        timeout: typing.Optional[int] = None,
        name: typing.Optional[str] = None,
        is_generator: typing.Optional[bool] = None,
        cloud: typing.Optional[str] = None,
        region: typing.Union[str, collections.abc.Sequence[str], None] = None,
        enable_memory_snapshot: bool = False,
        block_network: bool = False,
        restrict_modal_access: bool = False,
        max_inputs: typing.Optional[int] = None,
        i6pn: typing.Optional[bool] = None,
        include_source: typing.Optional[bool] = None,
        experimental_options: typing.Optional[dict[str, typing.Any]] = None,
        _experimental_scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
        _experimental_proxy_ip: typing.Optional[str] = None,
        _experimental_custom_scaling_factor: typing.Optional[float] = None,
        _experimental_enable_gpu_snapshot: bool = False,
        keep_warm: typing.Optional[int] = None,
        concurrency_limit: typing.Optional[int] = None,
        container_idle_timeout: typing.Optional[int] = None,
        allow_concurrent_inputs: typing.Optional[int] = None,
        _experimental_buffer_containers: typing.Optional[int] = None,
        allow_cross_region_volumes: typing.Optional[bool] = None,
    ) -> _FunctionDecoratorType:
        """Decorator to register a new Modal Function with this App."""
        ...

    @typing_extensions.dataclass_transform(
        field_specifiers=(modal.cls.parameter,),
        kw_only_default=True,
    )
    def cls(
        self,
        _warn_parentheses_missing: typing.Optional[bool] = None,
        *,
        image: typing.Optional[modal.image.Image] = None,
        secrets: collections.abc.Sequence[modal.secret.Secret] = (),
        gpu: typing.Union[None, str, modal.gpu._GPUConfig, list[typing.Union[None, str, modal.gpu._GPUConfig]]] = None,
        serialized: bool = False,
        network_file_systems: dict[
            typing.Union[str, pathlib.PurePosixPath], modal.network_file_system.NetworkFileSystem
        ] = {},
        volumes: dict[
            typing.Union[str, pathlib.PurePosixPath],
            typing.Union[modal.volume.Volume, modal.cloud_bucket_mount.CloudBucketMount],
        ] = {},
        cpu: typing.Union[float, tuple[float, float], None] = None,
        memory: typing.Union[int, tuple[int, int], None] = None,
        ephemeral_disk: typing.Optional[int] = None,
        min_containers: typing.Optional[int] = None,
        max_containers: typing.Optional[int] = None,
        buffer_containers: typing.Optional[int] = None,
        scaledown_window: typing.Optional[int] = None,
        proxy: typing.Optional[modal.proxy.Proxy] = None,
        retries: typing.Union[int, modal.retries.Retries, None] = None,
        timeout: typing.Optional[int] = None,
        cloud: typing.Optional[str] = None,
        region: typing.Union[str, collections.abc.Sequence[str], None] = None,
        enable_memory_snapshot: bool = False,
        block_network: bool = False,
        restrict_modal_access: bool = False,
        max_inputs: typing.Optional[int] = None,
        include_source: typing.Optional[bool] = None,
        experimental_options: typing.Optional[dict[str, typing.Any]] = None,
        _experimental_scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
        _experimental_proxy_ip: typing.Optional[str] = None,
        _experimental_custom_scaling_factor: typing.Optional[float] = None,
        _experimental_enable_gpu_snapshot: bool = False,
        keep_warm: typing.Optional[int] = None,
        concurrency_limit: typing.Optional[int] = None,
        container_idle_timeout: typing.Optional[int] = None,
        allow_concurrent_inputs: typing.Optional[int] = None,
        _experimental_buffer_containers: typing.Optional[int] = None,
        allow_cross_region_volumes: typing.Optional[bool] = None,
    ) -> collections.abc.Callable[[typing.Union[CLS_T, modal.partial_function.PartialFunction]], CLS_T]:
        """Decorator to register a new Modal [Cls](https://modal.com/docs/reference/modal.Cls) with this App."""
        ...

    def include(self, /, other_app: App) -> typing_extensions.Self:
        """Include another App's objects in this one.

        Useful for splitting up Modal Apps across different self-contained files.

        ```python
        app_a = modal.App("a")
        @app.function()
        def foo():
            ...

        app_b = modal.App("b")
        @app.function()
        def bar():
            ...

        app_a.include(app_b)

        @app_a.local_entrypoint()
        def main():
            # use function declared on the included app
            bar.remote()
        ```
        """
        ...

    class ___logs_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /, client: typing.Optional[modal.client.Client] = None) -> typing.Generator[str, None, None]:
            """Stream logs from the app.

            This method is considered private and its interface may change - use at your own risk!
            """
            ...

        def aio(
            self, /, client: typing.Optional[modal.client.Client] = None
        ) -> collections.abc.AsyncGenerator[str, None]:
            """Stream logs from the app.

            This method is considered private and its interface may change - use at your own risk!
            """
            ...

    _logs: ___logs_spec[typing_extensions.Self]

    @classmethod
    def _get_container_app(cls) -> typing.Optional[App]:
        """Returns the `App` running inside a container.

        This will return `None` outside of a Modal container.
        """
        ...

    @classmethod
    def _reset_container_app(cls):
        """Only used for tests."""
        ...

_default_image: modal.image._Image
