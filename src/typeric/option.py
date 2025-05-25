# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    option.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dfine <coding@dfine.tech>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/05/25 10:17:44 by dfine             #+#    #+#              #
#    Updated: 2025/05/25 10:17:46 by dfine            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from typing import (
    Generic,
    TypeAlias,
    TypeVar,
    Callable,
    NoReturn,
    final,
    override,
)

T = TypeVar("T")
U = TypeVar("U")


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

    def map(self, func: Callable[[T], U]) -> "Option[U]":
        return Some(func(self._value))

    def and_then(self, func: Callable[[T], "Option[U]"]) -> "Option[U]":
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

    def map(self, func: Callable[[T], U]) -> "NoneType":
        return NONE

    def and_then(self, func: Callable[[T], "Option[U]"]) -> "NoneType":
        return NONE

    @override
    def __eq__(self, other: object) -> bool:
        return isinstance(other, NoneType)

    @override
    def __repr__(self):
        return "None"


NONE = NoneType()
Option: TypeAlias = Some[T] | NoneType
