from dataclasses import dataclass
from typing import Any

from .transform import Transform


@dataclass
class Unknown:
    value: Any


@dataclass
class Invertible:
    value: Any


def maybe_negate(ex):
    def inner(negate):
        return (lambda s: s.neg(ex(s))) if negate else ex

    return Invertible(inner)


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
        return Invertible(
            lambda negate: lambda s: s.lit(-x) if negate else s.lit(x),
        )

    def neg(self, x):
        if isinstance(x, Invertible):
            return Invertible(lambda negate: x.value(not negate))
        return maybe_negate(self.bwd(x))

    def add(self, x, y):
        if isinstance(x, Invertible) and isinstance(y, Invertible):
            return Invertible(
                lambda negate: lambda s: s.add(x.value(negate)(s), y.value(negate)(s)),
            )
        return maybe_negate(lambda s: s.add(self.bwd(x)(s), self.bwd(y)(s)))

    def mul(self, x, y):
        if isinstance(x, Invertible):
            return Invertible(
                lambda negate: lambda s: s.mul(x.value(negate)(s), y.value(False)(s)),
            )
        if isinstance(y, Invertible):
            return Invertible(
                lambda negate: lambda s: s.mul(x.value(False)(s), y.value(negate)(s)),
            )
        return maybe_negate(lambda s: s.mul(self.bwd(x)(s), self.bwd(y)(s)))

    def sym(self, x):
        return maybe_negate(lambda s: s.sym(x))


push_neg = T.apply
