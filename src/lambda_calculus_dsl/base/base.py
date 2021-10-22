from abc import ABC, abstractmethod
from typing import Any, Callable


class Base(ABC):
    @abstractmethod
    def lit(self, x):
        ...

    @abstractmethod
    def neg(self, x):
        ...

    @abstractmethod
    def add(self, x, y):
        ...

    @abstractmethod
    def mul(self, x, y):
        ...

    def sub(self, x, y):
        return self.add(x, self.neg(y))


def lit(x) -> Callable[[Base], Any]:
    def ex(s: Base):
        return s.lit(x)

    return ex


def neg(x) -> Callable[[Base], Any]:
    def ex(s: Base):
        return s.neg(x(s))

    return ex


def add(x: Callable[[Base], Any], y: Callable[[Base], Any]) -> Callable[[Base], Any]:
    def ex(s: Base):
        return s.add(x(s), y(s))

    return ex


def mul(x: Callable[[Base], Any], y: Callable[[Base], Any]) -> Callable[[Base], Any]:
    def ex(s: Base):
        return s.mul(x(s), y(s))

    return ex


def sub(x: Callable[[Base], Any], y: Callable[[Base], Any]) -> Callable[[Base], Any]:
    def ex(s: Base):
        return s.sub(x(s), y(s))

    return ex
