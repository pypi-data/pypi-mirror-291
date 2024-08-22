from typing import Any, Callable
from dataclassabc import dataclassabc

from statemonad.statemonadtree.operations.flatmapmixin import FlatMapMixin
from statemonad.statemonadtree.operations.frommixin import FromMixin
from statemonad.statemonadtree.operations.getmixin import GetMixin
from statemonad.statemonadtree.operations.mapmixin import MapMixin
from statemonad.statemonadtree.operations.putmixin import PutMixin
from statemonad.statemonadtree.operations.zipmixin import ZipMixin
from statemonad.stateapplicative import StateApplicative


@dataclassabc(frozen=True)
class FlatMapImpl[State, U, ChildU](FlatMapMixin[State, U, ChildU]):
    child: StateApplicative[State, ChildU]
    func: Callable[[ChildU], StateApplicative[State, U]]


init_flat_map = FlatMapImpl


@dataclassabc(frozen=True)
class FromImpl[State, U](FromMixin[State, U]):
    value: U


init_from = FromImpl


@dataclassabc(frozen=True)
class GetImpl[State](GetMixin[State]):
    child: StateApplicative[State, Any]


init_get = GetImpl


@dataclassabc(frozen=True)
class MapImpl[State, U, ChildU](MapMixin[State, U, ChildU]):
    child: StateApplicative[State, ChildU]
    func: Callable[[ChildU], U]


init_map = MapImpl


@dataclassabc(frozen=True)
class PutImpl[State, U](PutMixin[State, U]):
    child: StateApplicative[State, U]
    state: State


init_put = PutImpl


@dataclassabc(frozen=True)
class ZipImpl[State, L, R](ZipMixin[State, L, R]):
    left: StateApplicative[State, L]
    right: StateApplicative[State, R]


init_zip = ZipImpl


