from abc import abstractmethod
from typing import Callable

from statemonad.statemonadtree.nodes import SingleChildStateMonadNode


class MapMixin[State, U, ChildU](SingleChildStateMonadNode[State, U, ChildU]):
    def __str__(self) -> str:
        return f'map({self.child}, {self.func})'

    @property
    @abstractmethod
    def func(self) -> Callable[[ChildU], U]:
        ...

    def apply(self, state: State) -> tuple[State, U]:
        state, value = self.child.apply(state)

        return state, self.func(value)
