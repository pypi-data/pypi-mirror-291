from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path  # noqa: TCH003
from typing import TYPE_CHECKING, assert_never

from utilities.pathlib import ensure_path
from utilities.platform import SYSTEM, System
from utilities.typed_settings import click_field

if TYPE_CHECKING:
    import datetime as dt


@dataclass(frozen=True)
class Config:
    """Settings for the `monitor_memory` script."""

    path: Path = click_field(
        default=ensure_path("memory.csv"), param_decls=("-p", "--path")
    )
    freq: int = click_field(default=60, help="in seconds", param_decls=("-f", "--freq"))
    duration: int | None = click_field(
        default=None, help="in seconds", param_decls=("-d", "--duration")
    )


@dataclass(frozen=True)
class ItemWindows:
    """A set of memory statistics."""

    datetime: dt.datetime
    virtual_total: int
    virtual_available: int
    virtual_percent: float
    virtual_used: int
    virtual_free: int
    swap_total: int
    swap_used: int
    swap_free: int
    swap_percent: float
    swap_sin: int
    swap_sout: int


@dataclass(frozen=True)
class ItemMacOS:
    """A set of memory statistics."""

    datetime: dt.datetime
    virtual_total: int
    virtual_available: int
    virtual_percent: float
    virtual_used: int
    virtual_free: int
    virtual_active: int
    virtual_inactive: int
    virtual_wired: int
    swap_total: int
    swap_used: int
    swap_free: int
    swap_percent: float
    swap_sin: int
    swap_sout: int


@dataclass(frozen=True)
class ItemLinux:
    """A set of memory statistics."""

    datetime: dt.datetime
    virtual_total: int
    virtual_available: int
    virtual_percent: float
    virtual_used: int
    virtual_free: int
    virtual_active: int
    virtual_inactive: int
    virtual_buffers: int
    virtual_cached: int
    virtual_shared: int
    virtual_slab: int
    swap_total: int
    swap_used: int
    swap_free: int
    swap_percent: float
    swap_sin: int
    swap_sout: int


match SYSTEM:
    case System.windows:  # skipif-os-ne-windows
        Item = ItemWindows
    case System.mac:  # skipif-os-ne-macos
        Item = ItemMacOS
    case System.linux:  # skipif-os-ne-linux
        Item = ItemLinux
    case _ as never:  # pyright: ignore[reportUnnecessaryComparison]
        assert_never(never)
