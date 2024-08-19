import typing as t

__all__ = ["AsyncFixture"]
_AsyncFixture = t.TypeVar("_AsyncFixture", covariant=True)


AsyncFixture = t.Callable[..., t.Awaitable[_AsyncFixture]]
