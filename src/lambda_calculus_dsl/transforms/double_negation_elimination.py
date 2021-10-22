from dataclasses import dataclass
from typing import Any

from .transform import Transform


@dataclass
class Keep:
    value: Any


@dataclass
class Negate:
    value: Any


class T(Transform):
    def fwd(self, x):
        return Keep(value=x)

    def bwd(self, x):
        if isinstance(x, Keep):
            return x.value
        elif isinstance(x, Negate):
            return lambda s: s.neg(x.value(s))
        raise AssertionError()

    def neg(self, x):
        if isinstance(x, Keep):
            return Negate(x.value)
        elif isinstance(x, Negate):
            return Keep(x.value)
        raise AssertionError()


double_neg_elimination = T.apply
