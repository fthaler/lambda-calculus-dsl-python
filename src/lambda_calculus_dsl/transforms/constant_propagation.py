from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from .transform import Transform


@dataclass
class Unknown:
    value: Any


@dataclass
class Literal:
    value: int


@dataclass
class Function:
    value: Callable


class T(Transform):
    def fwd(self, x):
        return Unknown(x)

    def bwd(self, x):
        if isinstance(x, Unknown):
            return x.value
        elif isinstance(x, Literal):
            return lambda s: s.lit(x.value)
        elif isinstance(x, Function):
            f = x.value
            return lambda s: s.lam(lambda x: self.bwd(f(self.fwd(lambda _: x)))(s))
        raise AssertionError()

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


constant_prop = T.apply
