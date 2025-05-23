# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    result.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dfine <coding@dfine.tech>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/05/23 12:46:18 by dfine             #+#    #+#              #
#    Updated: 2025/05/23 15:38:43 by dfine            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from collections.abc import Callable
from typing import Generic, NoReturn, TypeAlias, TypeVar, final, override

T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E", default=Exception)
F = TypeVar("F", default=Exception)


@final
class Ok(Generic[T]):
    _value: T
    __match_args__ = ("ok",)
    __slot__ = ("_value",)

    def __init__(self, value: T) -> None:
        self._value = value

    @override
    def __repr__(self):
        return f"Ok({self._value!r})"

    @property
    def ok(self) -> T:
        return self._value

    def is_ok(self):
        return True

    def is_err(self):
        return False

    def unwrap(self) -> T:
        return self._value

    def unwrap_or(self, default_value: T) -> T:
        return self._value

    def map(self, func: Callable[[T], U]) -> "Ok[U]":
        return Ok(func(self._value))

    def map_err(self, func: Callable[[E], F]) -> "Ok[T]":
        return self


class UnwrapError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


@final
class Err(Generic[E]):
    _value: E
    __match_args__ = ("err",)
    __slot__ = ("_value",)

    def __init__(self, error: E) -> None:
        self._value = error

    @override
    def __repr__(self):
        return f"Err({self._value!r})"

    @property
    def err(self) -> E:
        return self._value

    def is_ok(self):
        return False

    def is_err(self):
        return True

    def unwrap(self) -> NoReturn:
        if isinstance(self._value, BaseException):
            raise self._value
        raise UnwrapError(str(self._value))

    def unwrap_or(self, default_value: T) -> T:
        return default_value

    def map(self, func: Callable[[T], U]) -> "Err[E]":
        return self

    def map_err(self, func: Callable[[E], F]) -> "Err[F]":
        return Err(func(self._value))


Result: TypeAlias = Ok[T] | Err[E]
