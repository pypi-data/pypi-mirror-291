from abc import ABC, abstractmethod

from statemonad.stateapplicative import StateApplicative


class StateMonadNode[State, U](StateApplicative[State, U], ABC):
    pass


class SingleChildStateMonadNode[State, U, ChildU](StateMonadNode[State, U]):
    @property
    @abstractmethod
    def child(self) -> StateMonadNode[State, ChildU]: ...


class TwoChildrenStateMonadNode[State, U, L, R](StateMonadNode[State, U]):
    @property
    @abstractmethod
    def left(self) -> StateMonadNode[State, L]: ...

    @property
    @abstractmethod
    def right(self) -> StateMonadNode[State, R]: ...
