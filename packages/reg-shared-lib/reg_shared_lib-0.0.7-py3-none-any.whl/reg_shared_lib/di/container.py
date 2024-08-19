import typing as t

import punq

Service = t.TypeVar("Service")
_sentinel: t.Any = object()


class Container:
    __slots__ = ("_container",)

    def __init__(self) -> None:
        self._container = punq.Container()

    def register(
        self,
        service: t.Type[Service],
        *,
        instance: Service = _sentinel,
        factory: t.Callable[[], Service] = _sentinel,
        impl: t.Type[Service] = _sentinel,
        transient: bool = False,
    ) -> None:
        scope = punq.Scope.transient if transient else punq.Scope.singleton
        if instance is not _sentinel:
            self._container.register(service, instance=instance, scope=scope)
        elif factory is not _sentinel:
            self._container.register(service, factory=factory, scope=scope)
        elif impl is not _sentinel:
            self._container.register(service, factory=impl, scope=scope)
        else:
            self._container.register(service, factory=service, scope=scope)

    def resolve(self, service: t.Type[Service]) -> Service:
        return self._container.resolve(service)  # type: ignore[reportGeneralTypeIssues]

    def resolve_all(self, service: t.Type[Service]) -> list[Service]:
        return self._container.resolve_all(service)

    def create(self, service: t.Type[Service]) -> Service:
        return self._container.instantiate(service)  # type: ignore[reportGeneralTypeIssues]
