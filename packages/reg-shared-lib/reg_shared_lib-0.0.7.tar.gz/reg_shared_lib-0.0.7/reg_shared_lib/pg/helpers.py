import dataclasses
import typing as t

import sqlalchemy as sa

T = t.TypeVar("T")


@t.overload
def to_dataclass(cls: type[T], row: sa.Row) -> T:
    raise NotImplementedError


@t.overload
def to_dataclass(cls: type[T], row: sa.Row | None) -> T | None:
    raise NotImplementedError


def to_dataclass(cls: type[T], row: sa.Row | None) -> T | None:
    if not dataclasses.is_dataclass(cls):
        raise RuntimeError("%s is not a dataclass" % cls)
    if row is None:
        return None

    fields = dataclasses.fields(cls)
    result = cls(**{field.name: getattr(row, field.name) for field in fields if field.init})
    for field in [f for f in fields if not f.init]:
        setattr(result, field.name, getattr(row, field.name))
    return result  # type: ignore[return-value]


def to_dataclasses(cls: type[T], rows: t.Sequence[sa.Row]) -> list[T]:
    return [to_dataclass(cls, row) for row in rows]
