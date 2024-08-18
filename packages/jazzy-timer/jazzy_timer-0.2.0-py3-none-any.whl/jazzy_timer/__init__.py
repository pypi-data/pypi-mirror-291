""" \_\_init__.py for jazzy-timer. Contains the timer decorator.

## To use:

--------------------
from jazzy-timer import timer   

@timer   
def my_function():   
    # define function here   
    return result

result, elapsed_time = my_function()

---------------------
### Note that the result and the elapsed time are returned as a tuple. Once the decorator is added, you must unpack the tuple or you will get an error.

"""

import time
from functools import wraps
from typing import *

def timer(func = None, *, precision: int = 4) -> Callable[..., tuple[Any, float]]:
    """A decorator that times the execution of a function.
    
    :param precision: The number of decimal places to measure to.
    
    :return Callable[..., tuple[Any, float]]: A wrapped function that returns a tuple containing 
    the result of the function and the elapsed time in seconds.

    ```
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        elapsed_time = round(elapsed_time, precision)
        return result, elapsed_time
    return wrapper
    ```

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

    import logging
    logging.basicConfig(level=logging.INFO)

    @timer
    def test_function(time_to_sleep):

        time.sleep(time_to_sleep)
        return "some result", 33
    
    result, elapsed_time = test_function(3.43)
    print(f"Result of function call: {result} | Elapsed time: {elapsed_time} seconds")
    logging.info("Ran test_function with elapsed time: %s", elapsed_time)

    result, elapsed_time = test_function(0.543)
    print(f"Result of function call: {result} | Elapsed time: {elapsed_time} seconds")