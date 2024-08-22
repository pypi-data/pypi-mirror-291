
# State-Monad

State-Monad is a Python library that encapsulates stateful computations into a monadic structure.

## Overview

The state object (also referred to as a context) is a Python object that represents the state in your computations.
Each operation may modify the state and return a new values based on the updated state.
The result is a chain of operations where the state flows through each step, with the State-Monad keeping the flow clean and organized.

## Example

<!-- The following example illustrates the use of the State-Monad library. -->
In this example, we define the `collect_even_numbers` operations, which returns a `CollectEvenNumbers` state monad if the given number is even, or a default state monad encapsulating the value otherwise.
The `example` function performs monadic operations using the `collect_even_numbers` operator, resulting in a state monad.
Finally, the constructed state monad is applied with an empty tuple as the initial state.


``` python
from dataclassabc import dataclassabc

import statemonad
from statemonad.abc import StateMonadNode
from statemonad import init_state_monad


type State = tuple[int, ...]
state = tuple()


def collect_even_numbers(num: int):
    """
    This function encapsulates the given number within a state monad 
    and saves it to the state if the number is even.
    """
    
    if num % 2 == 0:

        @dataclassabc(frozen=True)
        class CollectEvenNumbers(StateMonadNode[State, int]):
            num: int

            def apply(self, state: State):
                n_state = state + (self.num,)
                return n_state, self.num

        return init_state_monad(CollectEvenNumbers(num=num))

    else:
        return statemonad.from_[State](num)

# do some monadic operations using `flat_map`
def example(init):
    return collect_even_numbers(init + 1).flat_map(
        lambda x: collect_even_numbers(x + 1).flat_map(
            lambda y: collect_even_numbers(y + 1).flat_map(
                lambda z: collect_even_numbers(z + 1)
            )
        )
    )

monad = example(3)

# Output will be
# monad=StateMonadImpl(
#   child=FlatMapImpl(
#       child=CollectEvenNumbers(num=4),
#   func=<function example.<locals>.<lambda> at 0x000001A546B53D80>))
print(f"{monad=}")

state, value = monad.apply(state)

print(f"{value=}")  # Output will be value=7
print(f"{state=}")  # Output will be state=(4, 6)
```

Note that defining the `CollectEvenNumbers` state monad as its proper class, enables us to nicely print the representation of the resulting Python object.
Unfortunately, parts of the representation is hidden behind the lambda function given to the `flat_map` method.


## Do-notation

Using the donotation library, the monadic sequence above can be rewritten with the do-notation as follows:

``` python
@do()
def example(init):
    x = yield from collect_even_numbers(init + 1)
    y = yield from collect_even_numbers(x + 1)
    z = yield from collect_even_numbers(y + 1)
    return collect_even_numbers(z + 1)
```



<!-- The following example illustrates how a state object `state` is created and used to compute an object `result`:


``` python
def compute_something(state):
    state, val1 = operation1(state)
    state, val2 = operation2(val1, state)
    state, result = operation2(val1, val2, state)
    return state, result

# Create state object used in the preceding computations.
state = init_state()

state, result1 = compute_something(state)
```

If we recompute the object, we can either use the same state object `state`,

``` python
# result2 might be different from result1, that is result1 != result3
state, result2 = compute_something(state)
```

or, we can create a new state object `state` resulting in the same object `result` as before:

``` python
# Create the same state object as before
state = init_state()

# result 1 == result 3
state, result3 = compute_something(state)
```
 -->
