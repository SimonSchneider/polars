from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import TYPE_CHECKING

import pytest

import polars as pl
from polars.utils import (
    _date_to_pl_date,
    _datetime_to_pl_timestamp,
    _timedelta_to_pl_timedelta,
    in_nanoseconds_window,
)

if TYPE_CHECKING:
    from polars.internals.type_aliases import TimeUnit


def test_in_ns_window() -> None:
    assert not in_nanoseconds_window(datetime(year=2600, month=1, day=1))
    assert in_nanoseconds_window(datetime(year=2000, month=1, day=1))


@pytest.mark.parametrize(
    "dt, tu, expected",
    [
        (datetime(2121, 1, 1), "ns", 4765132800000000000),
        (datetime(2121, 1, 1), "us", 4765132800000000),
        (datetime(2121, 1, 1), "ms", 4765132800000),
    ],
)
def test_datetime_to_pl_timestamp(dt: datetime, tu: TimeUnit, expected: int) -> None:
    out = _datetime_to_pl_timestamp(dt, tu)
    assert out == expected


def test_date_to_pl_date() -> None:
    d = date(1999, 9, 9)
    out = _date_to_pl_date(d)
    assert out == 10843


def test_timedelta_to_pl_timedelta() -> None:
    out = _timedelta_to_pl_timedelta(timedelta(days=1), "ns")
    assert out == 86_400_000_000_000
    out = _timedelta_to_pl_timedelta(timedelta(days=1), "us")
    assert out == 86_400_000_000
    out = _timedelta_to_pl_timedelta(timedelta(days=1), "ms")
    assert out == 86_400_000
    out = _timedelta_to_pl_timedelta(timedelta(days=1), tu=None)
    assert out == 86_400_000_000


def test_estimated_size() -> None:
    a = pl.Series([1, 2, 3])
    assert a.estimated_size() == a.to_frame().estimated_size()
