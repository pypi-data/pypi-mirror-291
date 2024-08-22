from __future__ import annotations

from abc import abstractmethod
from typing import Callable, override

from statemonad.statemonadtree.nodes import SingleChildStateMonadNode
from statemonad.statemonadtree.init import (
    init_flat_map,
    init_get,
    init_map,
    init_put,
    init_zip,
)
from statemonad.stateapplicative import StateApplicative


class StateMonad[State, U](
    SingleChildStateMonadNode[State, U, U]
):
    """
    This mixin class encapsulates stateful computations in a monadic context, allowing for state to be passed
    through a series of computations without explicitly threading it through function calls. This pattern is similar
    to the state monad found in functional programming languages.
    """

    @override
    def apply(self, state: State) -> tuple[State, U]:
        return self.child.apply(state)

    @abstractmethod
    def copy(self, /, **changes) -> StateMonad: ...

    # operations
    ############

    def flat_map[V](
        self, func: Callable[[U], StateApplicative[State, V]]
    ) -> StateMonad:
        return self.copy(child=init_flat_map(child=self.child, func=func))

    def get(self) -> StateMonad:
        return self.copy(child=init_get(child=self.child))

    def map[V](self, func: Callable[[U], V]) -> StateMonad:
        return self.copy(child=init_map(child=self.child, func=func))

    def put(self, state: State) -> StateMonad:
        return self.copy(child=init_put(child=self.child, state=state))

    def zip(self, other: StateMonad) -> StateMonad:
        return self.copy(child=init_zip(left=self.child, right=other.child))
