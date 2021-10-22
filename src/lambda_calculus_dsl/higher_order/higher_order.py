from abc import abstractmethod
from typing import Any, Callable

from ..base.base import Base


class HigherOrder(Base):
    @abstractmethod
    def lam(self, f):
        ...

    @abstractmethod
    def app(self, f, x):
        ...


def lam(f) -> Callable[[HigherOrder], Any]:
    def ex(s: HigherOrder) -> Callable[[HigherOrder], Any]:
        return s.lam(lambda x: f(lambda _: x)(s))

    return ex


def app(
    f: Callable[[HigherOrder], Any], x: Callable[[HigherOrder], Any]
) -> Callable[[HigherOrder], Any]:
    def ex(s: HigherOrder) -> Callable[[HigherOrder], Any]:
        return s.app(f(s), x(s))

    return ex
