from __future__ import annotations

from statemonad.stateapplicative import StateApplicative
from statemonad.statemonad.statemonad import StateMonad

def init_state_monad[State, U](
    child: StateApplicative[State, U],
) -> StateMonad[State, U]: ...
