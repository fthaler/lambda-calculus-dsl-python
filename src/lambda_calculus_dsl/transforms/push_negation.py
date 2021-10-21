from dataclasses import dataclass
import enum
from typing import Any

from .transform import Transform


@dataclass
class Unknown:
    value: Any


@dataclass
class Invertible:
    value: Any


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
        return super().neg(x)

    def add(self, x, y):
        if isinstance(x, Invertible) and isinstance(y, Invertible):
            return Invertible(
                lambda negate: lambda s: s.add(x.value(negate)(s), y.value(negate)(s)),
            )
        return super().add(x, y)

    def mul(self, x, y):
        if isinstance(x, Invertible) and isinstance(y, Invertible):
            return Invertible(
                lambda negate: lambda s: s.mul(x.value(negate)(s), y.value(False)(s)),
            )
        return super().mul(x, y)

    def sym(self, x):
        return Invertible(
            lambda negate: lambda s: s.neg(s.sym(x)) if negate else s.sym(x),
        )


push_neg = T.apply
