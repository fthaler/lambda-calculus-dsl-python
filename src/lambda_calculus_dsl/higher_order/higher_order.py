from abc import abstractmethod
from typing import Callable

from ..base.base import Base


class HigherOrder(Base):
    @abstractmethod
    def lam(self, f):
        ...

    @abstractmethod
    def app(self, f, x):
        ...


def lam(f) -> Callable[[HigherOrder], any]:
    def ex(s: HigherOrder) -> Callable[[HigherOrder], any]:
        return s.lam(lambda x: f(lambda _: x)(s))
    return ex


def app(f: Callable[[HigherOrder], any], x: Callable[[HigherOrder], any]) -> Callable[[HigherOrder], any]:
    def ex(s: HigherOrder) -> Callable[[HigherOrder], any]:
        return s.app(f(s), x(s))
    return ex
