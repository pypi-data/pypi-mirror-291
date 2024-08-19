import asyncio
import contextlib
import contextvars
import os
import sys
import typing as t
import uuid

from sqlalchemy.ext import asyncio as sa_async

context_conn = contextvars.ContextVar[sa_async.AsyncConnection | None](str(uuid.uuid4()), default=None)


class ConnectionContext:
    __slots__ = ("_engine",)

    @contextlib.asynccontextmanager
    async def acquire(self) -> t.AsyncIterator[sa_async.AsyncConnection]:
        if _context_conn := self._get_context_connection():
            yield _context_conn
        else:
            async with self._shielded_connection_with_transaction(self._engine) as conn:
                with self._set_context_connection(conn):
                    yield conn

    @staticmethod
    def _shielded_connection_with_transaction(
        engine: sa_async.AsyncEngine,
    ) -> t.AsyncContextManager[sa_async.AsyncConnection]:
        return ShieldedConnectionContext(engine.begin())

    @staticmethod
    def _get_context_connection() -> sa_async.AsyncConnection | None:
        return context_conn.get()

    @staticmethod
    @contextlib.contextmanager
    def _set_context_connection(conn: sa_async.AsyncConnection) -> t.Iterator[None]:
        token = context_conn.set(conn)
        try:
            yield
        finally:
            context_conn.reset(token)

    def __init__(self, engine: sa_async.AsyncEngine):
        self._engine = engine


class ShieldedConnectionContext(t.AsyncContextManager[sa_async.AsyncConnection]):
    __slots__ = ("_connection_ctx",)

    def __init__(self, connection_ctx: t.AsyncContextManager[sa_async.AsyncConnection]) -> None:
        self._connection_ctx = connection_ctx

    async def __aenter__(self) -> sa_async.AsyncConnection:
        aenter_task = asyncio.create_task(self._connection_ctx.__aenter__())
        try:
            return await asyncio.shield(aenter_task)
        except asyncio.CancelledError:
            await aenter_task
            await self._connection_ctx.__aexit__(*sys.exc_info())
            raise

    async def __aexit__(self, exc_type: t.Any, exc_val: t.Any, exc_tb: t.Any) -> None:
        await asyncio.shield(self._connection_ctx.__aexit__(exc_type, exc_val, exc_tb))


def get_connection_url(add_asyncpg_suffix: bool = True, default_db: str = "default_db") -> str:
    host = os.environ.get("DB_HOST", "localhost")
    port = int(os.environ.get("DB_PORT", 5432))
    user = os.environ.get("DB_USER", "postgres")
    password = os.environ.get("DB_PASSWORD", "")
    dbname = os.environ.get("DB_NAME", default_db)
    asyncpg_suffix = "+asyncpg" if add_asyncpg_suffix else ""

    url = f"postgresql{asyncpg_suffix}://{user}:{password}@{host}:{port}/{dbname}"
    return url
