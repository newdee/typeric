# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    option.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dfine <coding@dfine.tech>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/05/25 10:17:44 by dfine             #+#    #+#              #
#    Updated: 2025/05/27 22:17:56 by dfine            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from __future__ import annotations
from collections.abc import Awaitable
from functools import wraps
from typing import (
    Generic,
    ParamSpec,
    TypeAlias,
    TypeVar,
    Callable,
    NoReturn,
    final,
    override,
)

T = TypeVar("T")
U = TypeVar("U")
P = ParamSpec("P")
R = TypeVar("R")


class NoneTypeError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


@final
class Some(Generic[T]):
    __slots__ = ("_value",)
    __match_args__ = ("_value",)

    def __init__(self, value: T) -> None:
        self._value = value

    def is_some(self) -> bool:
        return True

    def is_none(self) -> bool:
        return False

    def unwrap(self) -> T:
        return self._value

    def unwrap_or(self, default: T) -> T:
        return self._value

    def map(self, func: Callable[[T], U]) -> Option[U]:
        return Some(func(self._value))

    def and_then(self, func: Callable[[T], Option[U]]) -> Option[U]:
        return func(self._value)

    @override
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Some) and self._value == other._value

    @override
    def __repr__(self):
        return f"Some({self._value!r})"


@final
class NoneType:
    __slots__ = ()
    __match_args__ = ()

    def is_some(self) -> bool:
        return False

    def is_none(self) -> bool:
        return True

    def unwrap(self) -> NoReturn:
        raise NoneTypeError("Called unwrap on a None value")

    def unwrap_or(self, default: T) -> T:
        return default

    def map(self, func: Callable[[T], U]) -> NoneType:
        return NONE

    def and_then(self, func: Callable[[T], Option[U]]) -> NoneType:
        return NONE

    @override
    def __eq__(self, other: object) -> bool:
        return isinstance(other, NoneType)

    @override
    def __repr__(self):
        return "None"


NONE = NoneType()
Option: TypeAlias = Some[T] | NoneType


def optiony(func: Callable[P, R]) -> Callable[P, Option[R]]:
    @wraps(func)
    def option_wrap(*args: P.args, **kwargs: P.kwargs) -> Option[R]:
        try:
            res = func(*args, **kwargs)
            return Some(res) if res is not None else NONE
        except Exception as _e:
            return NONE

    return option_wrap


def optiony_async(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[Option[R]]]:
    @wraps(func)
    async def option_wrap(*args: P.args, **kwargs: P.kwargs) -> Option[R]:
        try:
            res = await func(*args, **kwargs)
            return Some(res) if res is not None else NONE
        except Exception as _e:
            return NONE

    return option_wrap
