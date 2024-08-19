import typing as t

import sqlalchemy.ext.asyncio as sa_async


class FakeAsyncContextManager:
    __slots__ = ("obj",)

    def __init__(self, obj: sa_async.AsyncConnection) -> None:
        self.obj = obj

    async def __aenter__(self) -> sa_async.AsyncConnection:
        return self.obj

    def __await__(self) -> t.Generator:
        result = yield from self.wrap()  # type: ignore[misc]
        return result

    def wrap(self) -> sa_async.AsyncConnection:
        return self.obj

    async def __aexit__(self, exc_type: t.Any, exc: t.Any, tb: t.Any) -> None:
        pass
