from abc import abstractmethod
from typing import Callable

from statemonad.statemonadtree.nodes import SingleChildStateMonadNode
from statemonad.stateapplicative import StateApplicative

class FlatMapMixin[State, U, ChildU](SingleChildStateMonadNode[State, U, ChildU]):
    def __str__(self) -> str:
        return f'flat_map({self.child}, {self.func.__name__})'

    @property
    @abstractmethod
    def func(self) -> Callable[[ChildU], StateApplicative[State, U]]: ...

    def apply(self, state: State) -> tuple[State, U]:
        state, value = self.child.apply(state)

        return self.func(value).apply(state)
