from dataclasses import dataclass
from collections.abc import Callable
from typing import Any
from .transform import dummy_transform


@dataclass
class Unknown:
    value: Any


@dataclass
class Literal:
    value: int


@dataclass
class Function:
    value: Callable


def fwd(x):
    return Unknown(x)


def bwd(x):
    if isinstance(x, Unknown):
        return x.value
    elif isinstance(x, Literal):
        return lambda s: s.lit(x.value)
    elif isinstance(x, Function):
        f = x.value
        return lambda s: s.lam(lambda x: bwd(f(fwd(lambda _: x)))(s))
    raise AssertionError()


class T(dummy_transform(fwd, bwd)):
    @staticmethod
    def lit(x):
        return Literal(x)

    @staticmethod
    def neg(x):
        if isinstance(x, Literal):
            return Literal(-x.value)
        return super(T, T).neg(x)

    @staticmethod
    def add(x, y):
        if isinstance(x, Literal) and isinstance(y, Literal):
            return Literal(x.value + y.value)
        return super(T, T).add(x, y)

    @staticmethod
    def mul(x, y):
        if isinstance(x, Literal) and isinstance(y, Literal):
            return Literal(x.value * y.value)
        return super(T, T).mul(x, y)

    @staticmethod
    def lam(f):
        return Function(f)

    @staticmethod
    def app(f, x):
        if isinstance(f, Function):
            return f.value(x)
        return super(T, T).app(f, x)


def constant_prop(x):
    return bwd(x(T))
