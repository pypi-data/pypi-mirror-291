# tictactoc

A simple library to be able to control the time that certain parts of the code take

## Installation and use

To install this module use:

```sh
pip install tictactoc
```

Run tests to validate:

```sh
tictactoc-tests
```

## Usage

```py
from time import sleep
from tictactoc import tictactoc
from tictactoc import plot


# Basic use, start and end.
tictactoc.tic() # Start
print(tictactoc.toc()) # Finish

# Using tac in loops.
# We can do a tac in each iteration. When we finnish the loop, we do a toc skipping this time.

my_loop=["element1","element2","element3"]
tictactoc.tic("my loop")

for element in my_loop:
    sleep(0.1)
    tictactoc.tac("my loop")

result = tictactoc.toc("my loop", skip_toc=True)
print(f"total: {result["total"]}, each iteration: {', '.join(map(str,result["steps"]))}")
```

```plain
{'name': '__default', 'total': 5.0144999477197416e-05, 'steps': [5.0144999477197416e-05]}
total: 0.3002458430000843, each iteration: 0.10008363300039491, 0.10007859500001359, 0.10008361499967577
```

```py
# Print a plot.
# We can use the return value of toc for draw a plot.

plot.print(result)
```

```plain
========================================
my loop
--------------------
 0 | ###################
 1 | ###################
 2 | #################### !
--------------------
quantile value: 0.10020978839966119
========================================
```

## Credits

Developed and maintained by felipem775. [Contributions](CONTRIBUTING.md) are welcomed.
