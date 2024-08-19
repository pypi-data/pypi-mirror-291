import copy
import dataclasses
import typing as t

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
import sqlalchemy.ext.asyncio as sa_async
import sqlalchemy.orm as orm
import sqlalchemy.sql.dml as dml
from sqlalchemy.sql._typing import (  # type: ignore[reportPrivateUsage]
    _ColumnExpressionArgument,
    _ColumnExpressionOrStrLabelArgument,
)

from .connection import ConnectionContext
from .helpers import to_dataclass, to_dataclasses

_sentinel: t.Any = object()


@dataclasses.dataclass
class AbstractTable(t.Protocol):
    id: orm.Mapped[int]


T = t.TypeVar("T", bound=AbstractTable)


class AbstractRepo(t.Generic[T]):
    __slots__ = ("_conn_ctx",)
    _table: t.Type[T]

    @t.overload
    async def create(self, instance: T) -> T:
        raise NotImplementedError

    @t.overload
    async def create(self, **kwargs: t.Any) -> T:
        raise NotImplementedError

    async def create(self, *args: T, **kwargs: t.Any) -> T:
        instance = self._get_insert_instance(*args, **kwargs)
        query = self._build_insert_query(instance, ignore_conflicts=False)
        async with self._conn_ctx.acquire() as conn:
            result = await conn.execute(query)
            return to_dataclass(self._table, result.first())  # type: ignore[return-value]

    @t.overload
    async def create_or_none(self, instance: T) -> T | None:
        raise NotImplementedError

    @t.overload
    async def create_or_none(self, **kwargs: t.Any) -> T | None:
        raise NotImplementedError

    async def create_or_none(self, *args: T, **kwargs: t.Any) -> T | None:
        instance = self._get_insert_instance(*args, **kwargs)
        query = self._build_insert_query(instance, ignore_conflicts=True)
        async with self._conn_ctx.acquire() as conn:
            result = await conn.execute(query)
            return to_dataclass(self._table, result.first())

    @staticmethod
    def _get_insert_instance(*args: T, **kwargs: t.Any) -> dict[str, t.Any]:
        if len(args) == 1 and not kwargs:
            instance = {field.name: getattr(args[0], field.name) for field in dataclasses.fields(args[0]) if field.init}
        elif len(args) == 0 and kwargs:
            instance = copy.deepcopy(kwargs)
        else:
            raise RuntimeError("Ambiguous create")
        return instance

    def _build_insert_query(self, instance: dict[str, t.Any], ignore_conflicts: bool) -> dml.ReturningInsert:
        query = pg.insert(self._table).values(instance)
        if ignore_conflicts:
            query = query.on_conflict_do_nothing()
        query = query.returning(sa.literal_column("*"))  # type: ignore[assignment]
        return t.cast(dml.ReturningInsert, query)

    async def get_many(
        self,
        *clauses: _ColumnExpressionArgument[bool],
        order: _ColumnExpressionOrStrLabelArgument[t.Any] | None = _sentinel,
        conn: sa_async.AsyncConnection | None = None,
        limit: int | None = None,
        for_update: bool = False,
    ) -> list[T]:
        query = sa.select(self._table)
        if clauses:
            query = query.where(*clauses)
        if order is not _sentinel:
            query = query.order_by(order)
        if limit:
            query = query.limit(limit)
        if for_update:
            query = query.with_for_update()
        if conn is None:
            async with self._conn_ctx.acquire() as conn:
                result = await conn.execute(query)
        else:
            result = await conn.execute(query)
        return to_dataclasses(self._table, result.fetchall())

    async def get_one(
        self,
        *clauses: _ColumnExpressionArgument[bool],
        conn: sa_async.AsyncConnection | None = None,
        for_update: bool = False,
    ) -> T | None:
        instances = await self.get_many(*clauses, for_update=for_update, conn=conn)
        return next((i for i in instances), None)

    async def get(
        self,
        id: int,
        conn: sa_async.AsyncConnection | None = None,
        for_update: bool = False,
    ) -> T | None:
        return await self.get_one(self._table.id == id, conn=conn, for_update=for_update)

    async def update_many(self, *clauses: _ColumnExpressionArgument[bool], **update: t.Any) -> list[T]:
        if not clauses:
            raise RuntimeError("Can't update whole table")
        query = (
            sa.update(self._table)  # type: ignore[var-annotated]
            .where(*clauses)
            .values(update)
            .returning(sa.literal_column("*"))
        )
        async with self._conn_ctx.acquire() as conn:
            result = await conn.execute(query)
            return to_dataclasses(self._table, result.fetchall())

    async def update_one(self, clause: _ColumnExpressionArgument[bool], **update: t.Any) -> T | None:
        updated = await self.update_many(clause, **update)
        return next((u for u in updated), None)

    async def update(self, id: int, **update: t.Any) -> T | None:
        return await self.update_one(self._table.id == id, **update)

    async def delete_many(
        self,
        *clauses: _ColumnExpressionArgument[bool],
        conn: sa_async.AsyncConnection | None = None,
    ) -> list[T]:
        if not clauses:
            raise RuntimeError("Can't delete all")
        query = sa.delete(self._table).where(*clauses).returning(sa.literal_column("*"))  # type: ignore[var-annotated]
        if conn is None:
            async with self._conn_ctx.acquire() as conn:
                result = await conn.execute(query)
        else:
            result = await conn.execute(query)
        return to_dataclasses(self._table, result.fetchall())

    async def delete(self, id: int) -> T | None:
        deleted = await self.delete_many(self._table.id == id)
        return next((d for d in deleted), None)

    def __init__(self, conn_ctx: ConnectionContext) -> None:
        self._conn_ctx = conn_ctx
