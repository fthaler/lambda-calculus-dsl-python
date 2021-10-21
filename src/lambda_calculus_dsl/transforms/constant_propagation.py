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
    def lit(self, x):
        return Literal(x)

    def neg(self, x):
        if isinstance(x, Literal):
            return Literal(-x.value)
        return super().neg(x)

    def add(self, x, y):
        if isinstance(x, Literal) and isinstance(y, Literal):
            return Literal(x.value + y.value)
        return super().add(x, y)

    def mul(self, x, y):
        if isinstance(x, Literal) and isinstance(y, Literal):
            return Literal(x.value * y.value)
        return super().mul(x, y)

    def lam(self, f):
        return Function(f)

    def app(self, f, x):
        if isinstance(f, Function):
            return f.value(x)
        return super().app(f, x)


def constant_prop(x):
    return bwd(x(T()))
