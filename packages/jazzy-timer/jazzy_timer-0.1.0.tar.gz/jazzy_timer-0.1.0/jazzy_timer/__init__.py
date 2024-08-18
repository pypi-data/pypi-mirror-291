""" __init__.py for jazzy-timer. Contains the timer decorator. """


import time
from functools import wraps
from typing import *
import logging
logging.basicConfig(level=logging.INFO)

def timer(func = None, *, precision: int = 4) -> Callable[..., tuple[Any, float]]:
    """A decorator that times the execution of a function.
    
    :param precision: The number of decimal places to measure to.
    
    :return Callable[..., tuple[Any, float]]: A wrapped function that returns a tuple containing 
    the result of the function and the elapsed time in seconds.
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            elapsed_time = round(elapsed_time, precision)

            return result, elapsed_time
        return wrapper
    
    # If func is None, it means @timer() was used with parentheses
    if func is None:
        return decorator
    
    # If func is provided, it means @timer was used without parentheses
    return decorator(func)


if __name__ == "__main__":

    @timer
    def test_function(time_to_sleep):

        time.sleep(time_to_sleep)
        return "some result", 33
    
    result, elapsed_time = test_function(3.43)
    print(f"Result of function call: {result} | Elapsed time: {elapsed_time} seconds")
    logging.info("Ran test_function with elapsed time: %s", elapsed_time)

    result, elapsed_time = test_function(0.543)
    print(f"Result of function call: {result} | Elapsed time: {elapsed_time} seconds")