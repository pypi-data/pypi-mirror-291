import datetime
import decimal
import typing as t
import uuid

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

__all__ = ["type_annotation_map"]

type_annotation_map = {
    datetime.datetime: pg.TIMESTAMP(timezone=True),
    dict: pg.JSONB(none_as_null=True),  # type: ignore[no-untyped-call]
    dict[str, str]: pg.JSONB(none_as_null=True),  # type: ignore[no-untyped-call]
    uuid.UUID: pg.UUID(as_uuid=True),
    decimal.Decimal: pg.NUMERIC(),
    list[str]: pg.ARRAY(sa.String),
}
sentinel: t.Any = object()
