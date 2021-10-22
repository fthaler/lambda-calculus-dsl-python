from collections.abc import Callable
from dataclasses import dataclass

from toolz.functoolz import compose

from ..base.base import lit
from ..higher_order.higher_order import lam
from .transform import Transform


@dataclass
class Unknown:
    value: any


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
            return lit(x.value)
        elif isinstance(x, Function):
            return lam(compose(self.bwd, x.value, self.fwd))
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
