## jazzy-timer

Installation:
```
pip install jazzy-timer
```

*#1 in the "jazzy" utilities series by Edward Jazzhands.*
*Currently the only one in the series. More to come...*

A very simple timer that will return a tuple consisting of:
1) The result of the function call
2) The result of the timer (as a float)
   
This makes it much easier to format it to whatever you want, or use it for statistics:
- Send the two variables to different outputs (ie. send elapsed time to log output)
- Toggle displaying elapsed time on/off without removing the decorator.
- Compare times with other functions using math operators.
- Store the elapsed time in a database and sort ascending/descending.
- etc

### Why?

I found that the other simple timer libraries on PyPI do not work this way, and feel more convulted to use. 
This version is designed to be ultra-simple, and easier to integrate with other log systems you might be using.

### Examples:

Basic usage:
```
from jazzy-timer import timer

@timer
def func_to_be_timed():
    return something

result, elapsed_time = func_to_be_timed()   # returns a tuple

print(f"Result of function call: {result}")   # use function results as normal
logging.info("Ran func_to_be_timed with elapsed time: %s", elapsed_time)    # print elapsed time elsewhere
```

You can also set the timer precision (default is 4 decimal places). Timer can be used with or without this additional argument:
```
@timer(precision=2)
def func_to_be_timed():
    return something
```

If the function itself returns a tuple, you'll have a nested tuple:
```
@timer
def test_function(time_to_sleep):

    time.sleep(time_to_sleep)
    return "some result", 33

result_tuple, elapsed_time = test_function(0.543)
print(f"Result of function call: {result_tuple} | Elapsed time: {elapsed_time} seconds")
```
OUTPUT:
```
Result of function call: ('some result', 33) | Elapsed time: 0.5436 seconds
```
In this scenario, simply unpack the nested tuple in a separate step.

Thats it! There's nothing else to memorize. There's also no dependencies, it only uses standard library.

*All utilities in the "jazzy" series follow the Radical Simplicity design philosophy.*

