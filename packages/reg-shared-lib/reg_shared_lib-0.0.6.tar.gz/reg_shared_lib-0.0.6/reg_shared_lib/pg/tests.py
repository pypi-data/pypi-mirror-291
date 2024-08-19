import os
import typing as t

import pytest_service
import sqlalchemy.ext.asyncio as sa_async
from pytest import fixture

from ._fake_async_context import FakeAsyncContextManager
from .connection import ConnectionContext, get_connection_url

__all__ = ["FakeAsyncContextManager"]


@fixture(scope="session", autouse=True)
def init_env() -> None:
    os.environ["TZ"] = "UTC"


if os.getenv("MODE") == "ci":

    @fixture(scope="session")
    def init_pg() -> t.Iterable[pytest_service.PG]:  # type: ignore[reportRedeclaration]
        gitlab_service = pytest_service.PG(
            host=os.environ["DB_HOST"],
            port=5432,
            user=os.environ["DB_USER"],
            password="",
            database=os.environ["DB_NAME"],
        )
        yield gitlab_service

else:

    @fixture(scope="session")
    def init_pg(pg_16: pytest_service.PG) -> None:
        os.environ["DB_NAME"] = pg_16.database
        os.environ["DB_USER"] = pg_16.user
        os.environ["DB_PASSWORD"] = pg_16.password
        os.environ["DB_HOST"] = pg_16.host
        os.environ["DB_PORT"] = str(pg_16.port)


@fixture()
async def sa_engine(
    init_pg: pytest_service.PG,
) -> t.AsyncIterator[sa_async.AsyncEngine]:
    connection_url = get_connection_url()
    engine = sa_async.create_async_engine(
        connection_url,
        pool_size=int(os.getenv("POSTGRES_CONNECTIONS", 20)),
        pool_recycle=300,
        query_cache_size=0,
    )
    yield engine
    await engine.dispose()


@fixture()
def conn_context(sa_engine: sa_async.AsyncEngine) -> ConnectionContext:
    return ConnectionContext(sa_engine)
