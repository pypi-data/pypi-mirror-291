from typing import Callable, Any, Literal
from time import time
from datetime import timedelta
import logging
import sys


def simple_profile(function: Callable):
    """
    Decorator function that logs the execution time of the decorated function.

    Microseconds precision.

    Args:
        function (Callable): funtion to profile
    """

    def simple_profile_wrapper(*args, **kwargs):
        start = time()
        function(*args, **kwargs)
        end = time()
        execution_time = end - start
        logging.info(
            f"Function '{function.__name__}', execution time: {timedelta(microseconds=int(execution_time * 1000000))}"
        )

    return simple_profile_wrapper

def size_in_memory(object: Any, unit:Literal["gb", "mb", "kb"]) -> float | None:
    """
    Computes the size of an object in memory.

    Args:
        object (Any): the object whose memory usage is to be measured.
        unit (Literal[gb, mb, kb]): which unit of measure to use. Choose among kilobytes, megabytes and gigabytes.

    Returns:
        float | None: memory usage in the chosen unit of measure. None if the provided unit of measure is not valid.
    """
    if unit == "kb":
        memory = sys.getsizeof(object) / 1024
    elif unit == "mb":
        memory = sys.getsizeof(object) / 1024 / 1024
    elif unit == "gb":
        memory = sys.getsizeof(object) / 1024 / 1024 / 1024
    else:
        memory = None
        logging.error(f"Unknown unit '{unit}'. Please use one among: kb, mb, gb")
    return memory
