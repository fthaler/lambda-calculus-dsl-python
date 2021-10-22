from dataclasses import dataclass
from typing import Any

from .transform import Transform
from ..base.base import neg, lit, add, mul
from ..symbolic.symbolic import sym


@dataclass
class Unknown:
    value: Any


@dataclass
class Invertible:
    value: Any


def maybe_negate_(ex):
    return Invertible(lambda negate: neg(ex) if negate else ex)


def maybe_negate(ex):
    return lambda negate: neg(ex) if negate else ex


class T(Transform):
    def fwd(self, x):
        assert not isinstance(x, (Unknown, Invertible))

        def f(negate):
            assert not negate
            return x

        return Unknown(f)

    def bwd(self, x):
        assert isinstance(x, (Unknown, Invertible))
        return x.value(False)

    def lit(self, x):
        return Invertible(lambda negate: lit(-x) if negate else lit(x))

    def neg(self, x):
        return Invertible(
            (lambda negate: x.value(not negate))
            if isinstance(x, Invertible)
            else maybe_negate(x)
        )

    def add(self, x, y):
        return Invertible(
            (lambda negate: add(x.value(negate), y.value(negate)))
            if isinstance(x, Invertible) and isinstance(y, Invertible)
            else maybe_negate(add(self.bwd(x), self.bwd(y)))
        )

    def mul(self, x, y):
        return Invertible(
            (lambda negate: mul(x.value(negate), y.value(False)))
            if isinstance(x, Invertible)
            else (lambda negate: mul(x.value(False), y.value(negate)))
            if isinstance(y, Invertible)
            else maybe_negate(lambda s: s.mul(self.bwd(x)(s), self.bwd(y)(s)))
        )

    def sym(self, x):
        return Invertible(maybe_negate(sym(x)))


push_neg = T.apply
