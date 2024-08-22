from collections.abc import Iterable
from typing import Any, Callable, Generator

from statemonad.statemonad.statemonad import StateMonad as _StateMonad
from statemonad.statemonad.from_ import from_ as _from_, get as _get
from statemonad.statemonad.init import init_state_monad as _init_state_monad

from_ = _from_
get = _get
put = from_(None).put

init_state_monad = _init_state_monad


def do():
    def decorator[V](fn: Callable[..., Generator[Any, None, V]]):
        def wrapper(*args, **kwargs) -> V:
            gen = fn(*args, **kwargs)

            def send_and_yield(value):
                try:
                    next_val = gen.send(value)
                except StopIteration as e:
                    result = e.value
                else:
                    result = next_val.flat_map(send_and_yield)
                return result

            return send_and_yield(None)
        return wrapper
    return decorator


# def for_each[U](elems: Iterable[U]):
    
#     def decorator[State: _StateCache, V](func: Callable[[U], Generator[None, None, _StateMonad[State, V]]]):
#         do_func = do()(func)

#         def dec_func():
#             return zip(do_func(elem) for elem in elems)

#         return wraps(func)(dec_func)  # type: ignore
    
#     return decorator


def zip[State, U](others: Iterable[_StateMonad[State, U]]) -> _StateMonad[State, tuple[U, ...]]:
    others = iter(others)
    try:
        current = next(others).map(lambda v: (v,))
    except StopIteration:
        return from_(tuple())
    else:
        for other in others:
            current = current.zip(other).map(lambda v: v[0] + (v[1],))
        return current
