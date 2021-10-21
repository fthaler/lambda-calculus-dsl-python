from dataclasses import dataclass
from typing import Any
from .transform import dummy_transform


@dataclass
class Unknown:
    value: Any


@dataclass
class Invertible:
    value: Any


def fwd(x):
    def f(negate):
        assert not negate
        return x

    return Unknown(value=f)


def bwd(x):
    assert isinstance(x, (Unknown, Invertible))
    return x.value(False)


class T(dummy_transform(fwd, bwd)):
    def lit(self, x):
        return Invertible(lambda negate: lambda s: s.lit(-x) if negate else s.lit(x))

    def neg(self, x):
        assert isinstance(x, Invertible)
        return Invertible(lambda negate: x.value(not negate))

    def add(self, x, y):
        assert isinstance(x, Invertible) and isinstance(y, Invertible)
        return Invertible(
            lambda negate: lambda s: s.add(x.value(negate)(s), y.value(negate)(s))
        )

    def mul(self, x, y):
        assert isinstance(x, Invertible) and isinstance(y, Invertible)
        return Invertible(
            lambda negate: lambda s: s.mul(x.value(negate)(s), y.value(False)(s))
        )

    def sym(self, x):
        return Invertible(
            lambda negate: lambda s: s.neg(s.sym(x)) if negate else s.sym(x)
        )


def push_neg(x):
    return bwd(x(T()))
