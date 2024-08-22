from __future__ import annotations

from dataclasses import replace
from typing import override
from dataclassabc import dataclassabc

from statemonad.statemonad.statemonad import StateMonad
from statemonad.stateapplicative import StateApplicative


@dataclassabc(frozen=True)
class StateMonadImpl[State, U](StateMonad[State, U]):
    child: StateApplicative[State, U]

    def __str__(self) -> str:
        return f"StateMonad({self.child})"

    @override
    def copy(self, /, **changes) -> StateMonad[State, U]:
        return replace(self, **changes)


init_state_monad = StateMonadImpl
# def init_state_monad[State: StateCache, U](child: StateApplicative[State, U]):
#     return StateMonadImpl(child=child)
