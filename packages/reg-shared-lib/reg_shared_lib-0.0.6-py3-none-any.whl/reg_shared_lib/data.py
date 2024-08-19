import dataclasses
import datetime
import typing as t

import pytz


@dataclasses.dataclass
class Event:
    id: int
    slug: str
    year: str
    event_date_start: datetime.date
    event_date_stop: datetime.date
    _timezone: str
    name: str
    instrumental: str

    @property
    def event_slug(self) -> str:
        return f"{self.slug}{self.year}"

    @property
    def timezone(self) -> datetime.timezone:
        result = (
            datetime.timezone(datetime.timedelta(hours=3), name="Europe/Moscow")
            if self._timezone == "Europe/Moscow"
            else pytz.timezone(self._timezone)
        )
        return t.cast(datetime.timezone, result)


@dataclasses.dataclass
class User:
    id: int
    first_name: str
    last_name: str
    sname: str
    nickname: str
    repr: str
    telegram_id: str | None
    telegram_username: str | None
    telegram_first_name: str | None
    telegram_last_name: str | None
    rus_youth_id: str | None

    def get_with_repr(self) -> str:
        if self.repr == "":
            return self.get_full_name_with_nick()
        else:
            return "(#{id}) {repr}".format(id=self.id, repr=self.repr)

    def get_full_name_with_nick(self) -> str:
        return "(#{id}) {first_name}{nickname} {last_name}".format(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            nickname=f' "{self.nickname}"' if self.nickname else "",
        )

    def get_full_name(self):
        return " ".join([i for i in (self.first_name, self.sname, self.last_name) if i])
