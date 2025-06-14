# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    wrap_funcs.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dfine <coding@dfine.tech>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/05/12 11:44:04 by dfine             #+#    #+#              #
#    Updated: 2025/05/12 11:44:05 by dfine            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from collections.abc import Awaitable
from functools import wraps
from time import perf_counter
from typing import Callable, ParamSpec, TypeVar

from loguru import logger

P = ParamSpec("P")
R = TypeVar("R")


def get_time_async(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
    @wraps(func)
    async def timed_execution(*args: P.args, **kwargs: P.kwargs) -> R:
        logger.info(f"Starting async func@{func.__name__} with {args= }, {kwargs= }")
        try:
            start_time = perf_counter()
            result = await func(*args, **kwargs)
            end_time = perf_counter()
            logger.info(f"{func.__name__} took {end_time - start_time:.3f}s")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} failed with exception: {e}")
            raise

    return timed_execution


def get_time_sync(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def timed_execution(*args: P.args, **kwargs: P.kwargs) -> R:
        logger.info(f"Starting sync func@{func.__name__} with {args= }, {kwargs= }")
        try:
            start_time = perf_counter()
            result = func(*args, **kwargs)
            end_time = perf_counter()
            logger.info(f"{func.__name__} took {end_time - start_time:.3f}s")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} failed with exception: {e}")
            raise

    return timed_execution
