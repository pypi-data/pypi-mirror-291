import inspect
from asyncio import to_thread
from collections.abc import Awaitable, Callable
from functools import wraps
from inspect import iscoroutinefunction, isfunction
from typing import Any, Literal, ParamSpec, TypeVar

__all__ = ["SizeUnit", "make_async", "scale_bytes", "to_async"]

_T = TypeVar("_T")
_P = ParamSpec("_P")


def to_async(func: Callable[_P, _T]) -> Callable[..., Awaitable[_T]]:
    """
    Allows a blocking function to be executed asynchronously by wrapping it in a call to to_thread of the asyncio library.

    Args:
        func (Callable[_P, _T]): function with a blocking call.

    Returns:
        Callable: a function that returns a awaitable object.
    """

    @wraps(func)
    def wrapped(*args: _P.args, **kwargs: _P.kwargs) -> Awaitable[_T]:
        return to_thread(func, *args, **kwargs)

    return wrapped


def make_async(cls: type[Any]) -> type:
    """
    The decorator converts all class methods to an asynchronous version using another decorating function, to_async.

    Args:
        cls (type[Any]): the class whose methods need to be patched.

    Returns:
        type: a class with methods converted to an asynchronous version.
    """
    members: list[tuple[str, Callable]] = inspect.getmembers(cls, isfunction)
    for name, meth in members:
        if not name.startswith("__"):
            if iscoroutinefunction(meth):
                continue
            setattr(cls, name, to_async(meth))  # type: ignore
    return cls


SizeUnit = Literal[
    "b", "bytes", "kb", "kilobytes", "mb", "megabytes", "gb", "gigabytes"
]
"""
Available data size units.
"""


def scale_bytes(sz: int | float, unit: SizeUnit) -> int | float:
    """Scale size in bytes to other size units (eg: "kb", "mb", "gb", "tb")."""
    if unit in {"b", "bytes"}:
        return sz
    elif unit in {"kb", "kilobytes"}:
        return sz / 1024
    elif unit in {"mb", "megabytes"}:
        return sz / 1024**2
    elif unit in {"gb", "gigabytes"}:
        return sz / 1024**3
    else:
        raise ValueError(
            f"`unit` must be one of {{'b', 'kb', 'mb', 'gb', 'tb'}}, got {unit!r}"
        )


if __name__ == "__name__":
    ...
