import modal.client
import typing
import typing_extensions

class _FlashManager:
    def __init__(self, client: modal.client._Client, port: int, health_check_url: typing.Optional[str] = None):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    async def _start(self): ...
    async def _run_heartbeat(self, host: str, port: int): ...
    def get_container_url(self): ...
    async def stop(self): ...
    async def close(self): ...

SUPERSELF = typing.TypeVar("SUPERSELF", covariant=True)

class FlashManager:
    def __init__(self, client: modal.client.Client, port: int, health_check_url: typing.Optional[str] = None): ...

    class ___start_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /): ...
        async def aio(self, /): ...

    _start: ___start_spec[typing_extensions.Self]

    class ___run_heartbeat_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /, host: str, port: int): ...
        async def aio(self, /, host: str, port: int): ...

    _run_heartbeat: ___run_heartbeat_spec[typing_extensions.Self]

    def get_container_url(self): ...

    class __stop_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /): ...
        async def aio(self, /): ...

    stop: __stop_spec[typing_extensions.Self]

    class __close_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /): ...
        async def aio(self, /): ...

    close: __close_spec[typing_extensions.Self]

class __flash_forward_spec(typing_extensions.Protocol):
    def __call__(self, /, port: int, health_check_url: typing.Optional[str] = None) -> FlashManager:
        """Forward a port to the Modal Flash service, exposing that port as a stable web endpoint.

        This is a highly experimental method that can break or be removed at any time without warning.
        Do not use this method unless explicitly instructed to do so by Modal support.
        """
        ...

    async def aio(self, /, port: int, health_check_url: typing.Optional[str] = None) -> FlashManager:
        """Forward a port to the Modal Flash service, exposing that port as a stable web endpoint.

        This is a highly experimental method that can break or be removed at any time without warning.
        Do not use this method unless explicitly instructed to do so by Modal support.
        """
        ...

flash_forward: __flash_forward_spec

class _FlashPrometheusAutoscaler:
    def __init__(
        self,
        client: modal.client._Client,
        app_name: str,
        cls_name: str,
        metrics_endpoint: str,
        target_metric: str,
        target_metric_value: float,
        min_containers: typing.Optional[int],
        max_containers: typing.Optional[int],
        scale_up_tolerance: float,
        scale_down_tolerance: float,
        scale_up_stabilization_window_seconds: int,
        scale_down_stabilization_window_seconds: int,
        autoscaling_interval_seconds: int,
    ):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    async def start(self): ...
    async def _run_autoscaler_loop(self): ...
    async def _compute_target_containers(self, current_replicas: int) -> int: ...
    async def _get_metrics(self, url: str) -> typing.Optional[dict[str, list[typing.Any]]]: ...
    async def _get_all_containers(self): ...
    def _make_scaling_decision(
        self,
        current_replicas: int,
        autoscaling_decisions: list[tuple[float, int]],
        scale_up_stabilization_window_seconds: int = 0,
        scale_down_stabilization_window_seconds: int = 300,
        min_containers: typing.Optional[int] = None,
        max_containers: typing.Optional[int] = None,
    ) -> int:
        """Return the target number of containers following (simplified) Kubernetes HPA
        stabilization-window semantics.

        Args:
            current_replicas: Current number of running Pods/containers.
            autoscaling_decisions: List of (timestamp, desired_replicas) pairs, where
                                   timestamp is a UNIX epoch float (seconds).
                                   The list *must* contain at least one entry and should
                                   already include the most-recent measurement.
            scale_up_stabilization_window_seconds: 0 disables the up-window.
            scale_down_stabilization_window_seconds: 0 disables the down-window.
            min_containers / max_containers: Clamp the final decision to this range.

        Returns:
            The target number of containers.
        """
        ...

    async def stop(self): ...

class FlashPrometheusAutoscaler:
    def __init__(
        self,
        client: modal.client.Client,
        app_name: str,
        cls_name: str,
        metrics_endpoint: str,
        target_metric: str,
        target_metric_value: float,
        min_containers: typing.Optional[int],
        max_containers: typing.Optional[int],
        scale_up_tolerance: float,
        scale_down_tolerance: float,
        scale_up_stabilization_window_seconds: int,
        scale_down_stabilization_window_seconds: int,
        autoscaling_interval_seconds: int,
    ): ...

    class __start_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /): ...
        async def aio(self, /): ...

    start: __start_spec[typing_extensions.Self]

    class ___run_autoscaler_loop_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /): ...
        async def aio(self, /): ...

    _run_autoscaler_loop: ___run_autoscaler_loop_spec[typing_extensions.Self]

    class ___compute_target_containers_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /, current_replicas: int) -> int: ...
        async def aio(self, /, current_replicas: int) -> int: ...

    _compute_target_containers: ___compute_target_containers_spec[typing_extensions.Self]

    class ___get_metrics_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /, url: str) -> typing.Optional[dict[str, list[typing.Any]]]: ...
        async def aio(self, /, url: str) -> typing.Optional[dict[str, list[typing.Any]]]: ...

    _get_metrics: ___get_metrics_spec[typing_extensions.Self]

    class ___get_all_containers_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /): ...
        async def aio(self, /): ...

    _get_all_containers: ___get_all_containers_spec[typing_extensions.Self]

    def _make_scaling_decision(
        self,
        current_replicas: int,
        autoscaling_decisions: list[tuple[float, int]],
        scale_up_stabilization_window_seconds: int = 0,
        scale_down_stabilization_window_seconds: int = 300,
        min_containers: typing.Optional[int] = None,
        max_containers: typing.Optional[int] = None,
    ) -> int:
        """Return the target number of containers following (simplified) Kubernetes HPA
        stabilization-window semantics.

        Args:
            current_replicas: Current number of running Pods/containers.
            autoscaling_decisions: List of (timestamp, desired_replicas) pairs, where
                                   timestamp is a UNIX epoch float (seconds).
                                   The list *must* contain at least one entry and should
                                   already include the most-recent measurement.
            scale_up_stabilization_window_seconds: 0 disables the up-window.
            scale_down_stabilization_window_seconds: 0 disables the down-window.
            min_containers / max_containers: Clamp the final decision to this range.

        Returns:
            The target number of containers.
        """
        ...

    class __stop_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /): ...
        async def aio(self, /): ...

    stop: __stop_spec[typing_extensions.Self]

class __flash_prometheus_autoscaler_spec(typing_extensions.Protocol):
    def __call__(
        self,
        /,
        app_name: str,
        cls_name: str,
        metrics_endpoint: str,
        target_metric: str,
        target_metric_value: float,
        min_containers: typing.Optional[int] = None,
        max_containers: typing.Optional[int] = None,
        scale_up_tolerance: float = 0.1,
        scale_down_tolerance: float = 0.1,
        scale_up_stabilization_window_seconds: int = 0,
        scale_down_stabilization_window_seconds: int = 300,
        autoscaling_interval_seconds: int = 15,
    ) -> FlashPrometheusAutoscaler:
        """Autoscale a Flash service based on containers' Prometheus metrics.

        The package `prometheus_client` is required to use this method.

        This is a highly experimental method that can break or be removed at any time without warning.
        Do not use this method unless explicitly instructed to do so by Modal support.
        """
        ...

    async def aio(
        self,
        /,
        app_name: str,
        cls_name: str,
        metrics_endpoint: str,
        target_metric: str,
        target_metric_value: float,
        min_containers: typing.Optional[int] = None,
        max_containers: typing.Optional[int] = None,
        scale_up_tolerance: float = 0.1,
        scale_down_tolerance: float = 0.1,
        scale_up_stabilization_window_seconds: int = 0,
        scale_down_stabilization_window_seconds: int = 300,
        autoscaling_interval_seconds: int = 15,
    ) -> FlashPrometheusAutoscaler:
        """Autoscale a Flash service based on containers' Prometheus metrics.

        The package `prometheus_client` is required to use this method.

        This is a highly experimental method that can break or be removed at any time without warning.
        Do not use this method unless explicitly instructed to do so by Modal support.
        """
        ...

flash_prometheus_autoscaler: __flash_prometheus_autoscaler_spec

class __flash_get_containers_spec(typing_extensions.Protocol):
    def __call__(self, /, app_name: str, cls_name: str) -> list[dict[str, typing.Any]]:
        """Return a list of flash containers for a deployed Flash service.

        This is a highly experimental method that can break or be removed at any time without warning.
        Do not use this method unless explicitly instructed to do so by Modal support.
        """
        ...

    async def aio(self, /, app_name: str, cls_name: str) -> list[dict[str, typing.Any]]:
        """Return a list of flash containers for a deployed Flash service.

        This is a highly experimental method that can break or be removed at any time without warning.
        Do not use this method unless explicitly instructed to do so by Modal support.
        """
        ...

flash_get_containers: __flash_get_containers_spec
