# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_result.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dfine <coding@dfine.tech>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/05/23 12:46:20 by dfine             #+#    #+#              #
#    Updated: 2025/05/27 22:17:42 by dfine            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import asyncio
import hashlib
from functools import partial
from pathlib import Path
from typing import BinaryIO

import pytest

from typeric.result import (
    Err,
    Ok,
    Result,
    UnwrapError,
    resulty,
    resulty_async,
    spreadable,
    spreadable_async,
)


def get_md5(file_obj: BinaryIO) -> Result[str, Exception]:
    md5 = hashlib.md5()
    try:
        while chunk := file_obj.read(8096):
            md5.update(chunk)
        _ = file_obj.seek(0)
        return Ok(md5.hexdigest())
    except Exception as e:
        return Err(e)


def is_exist(element: str, file_sets: set[str], auto_add: bool = True) -> bool:
    exist = element in file_sets
    if not exist and auto_add:
        file_sets.add(element)
    return exist


def file_exist(
    file_obj: BinaryIO, file_sets: set[str], auto_add: bool = True
) -> Result[bool, Exception]:
    match get_md5(file_obj):
        case Ok(md5):
            print(md5)
        case Err(e):
            print(f"error occurred: {e}")
    func = partial(is_exist, file_sets=file_sets, auto_add=auto_add)
    return get_md5(file_obj).map(func=func)


def test_file() -> None:
    file_set: set[str] = set()
    file_path = [Path("test1.pdf"), Path("test1.pdf"), Path("test2.pdf")]
    for file in file_path:
        with open(file, "rb") as f:
            exist = file_exist(f, file_set)
            assert exist.is_ok()


def test_ok_basic():
    result = Ok(10)
    assert result.is_ok()
    assert not result.is_err()
    assert result.unwrap() == 10
    assert result.unwrap_or(0) == 10
    assert result.unwrap_or_else(lambda _: 0) == 10
    assert result.map(lambda x: x + 1) == Ok(11)
    assert result.map_err(lambda e: f"error: {e}") == Ok(10)
    assert result.and_then(lambda x: Ok(x * 2)) == Ok(20)
    assert result.or_else(lambda e: Err("fallback")) == Ok(10)

    output = []
    result.inspect(lambda x: output.append(x))
    assert output == [10]


def plus_one(x: int) -> int:
    return x + 1


def times_two(x: int) -> Ok[int]:
    return Ok(x * 2)


def test_err_basic():
    result = Err("failure")
    assert not result.is_ok()
    assert result.is_err()
    assert result.unwrap_or(99) == 99
    assert result.unwrap_or_else(lambda e: 42) == 42
    assert result.map(plus_one) == result
    assert result.map_err(str.upper) == Err("FAILURE")
    assert result.and_then(times_two) == result
    assert result.or_else(lambda e: Ok("fallback")) == Ok("fallback")

    output = []
    result.inspect_err(lambda e: output.append(e))
    assert output == ["failure"]


def test_err_raises_exception():
    result = Err(ValueError("bad"))
    with pytest.raises(ValueError, match="bad"):
        result.unwrap()


def test_err_raises_unwraperror_if_not_exception():
    result = Err("not an exception")
    with pytest.raises(UnwrapError, match="not an exception"):
        result.unwrap()


def test_result_equality_and_hash():
    assert Ok(1) == Ok(1)
    assert Err("x") == Err("x")
    assert Ok(1) != Err(1)
    assert hash(Ok(1)) == hash(Ok(1))
    assert hash(Err("x")) == hash(Err("x"))


def test_match_args():
    match Ok("yes"):
        case Ok(value):
            assert value == "yes"
        case _:
            assert False

    match Err("oops"):
        case Err(error):
            assert error == "oops"
        case _:
            assert False


def func_a(x: int) -> Result[int, str]:
    if x < 0:
        return Err("negative input")
    return Ok(x * 2)


@spreadable
def func_b(y: int) -> Result[int, str]:
    a = func_a(y).spread()
    return Ok(a + 1)


def test_func_b_success():
    assert func_b(5) == Ok(11)  # 5*2=10 +1=11


def test_func_b_propagate_error():
    assert func_b(-2) == Err("negative input")


async def async_func_a(x: int) -> Result[int, str]:
    if x < 0:
        return Err("negative input")
    return Ok(x * 2)


@spreadable_async
async def async_func_b(y: int) -> Result[int, str]:
    a = (await async_func_a(y)).spread()
    return Ok(a + 1)


@pytest.mark.asyncio
async def test_async_func_b_success():
    result = await async_func_b(5)
    assert result == Ok(11)


@pytest.mark.asyncio
async def test_async_func_b_propagate_error():
    result = await async_func_b(-2)
    assert result == Err("negative input")


def test_ok_combine_ok():
    res1 = Ok("user")
    res2 = Ok(18)
    res3 = Ok("email@example.com")

    combined = res1.combine(res2).combine(res3)

    assert isinstance(combined, Ok)
    assert combined.unwrap() == (("user", 18), "email@example.com")


def test_ok_combine_err():
    res1 = Ok("user")
    res2 = Err("age is invalid")

    combined = res1.combine(res2)

    assert isinstance(combined, Err)
    assert combined.err == "age is invalid"
    assert combined.errs == ["age is invalid"]


def test_err_combine_err_chain():
    err1 = Err("invalid name")
    err2 = Err("invalid age")
    err3 = Err("invalid email")

    combined = err1.combine(err2).combine(err3)

    assert isinstance(combined, Err)
    assert combined.err == "invalid name"
    assert combined.errs == ["invalid name", "invalid age", "invalid email"]


def test_err_combine_ok_no_effect():
    err = Err("something wrong")
    ok = Ok("good")

    combined = err.combine(ok)

    assert isinstance(combined, Err)
    assert combined.err == "something wrong"
    assert combined.errs == ["something wrong"]


@resulty
def div(x: int, y: int) -> float:
    return x / y


def test_resulty_ok():
    result = div(10, 2)
    assert isinstance(result, Ok)
    assert result.unwrap() == 5.0


def test_resulty_err():
    result = div(10, 0)
    assert isinstance(result, Err)
    assert "division by zero" in str(result.err)


@resulty_async
async def async_div(x: int, y: int) -> float:
    await asyncio.sleep(0.01)
    return x / y


@pytest.mark.asyncio
async def test_async_resulty_ok():
    result = await async_div(8, 2)
    assert isinstance(result, Ok)
    assert result.unwrap() == 4.0


@pytest.mark.asyncio
async def test_async_resulty_err():
    result = await async_div(5, 0)
    assert isinstance(result, Err)
    assert "division by zero" in str(result.err)


def test_resulty_overload():
    @resulty
    def f1(x: int) -> int:
        return x * 2

    @resulty
    def f2(x: int) -> Result[int, ValueError]:
        if x < 0:
            return Err(ValueError("neg"))
        return Ok(x)

    r1 = f1(3)
    r2 = f2(-1)
    r3 = f2(5)

    assert r1 == Ok(6)
    assert r2 == Err("neg")
    assert r3 == Ok(5)
