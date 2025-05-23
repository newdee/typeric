# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_result.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dfine <coding@dfine.tech>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/05/23 12:46:20 by dfine             #+#    #+#              #
#    Updated: 2025/05/23 15:50:13 by dfine            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from functools import partial
import hashlib
from pathlib import Path
from typing import BinaryIO

from typeric.result import Result, Ok, Err


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
