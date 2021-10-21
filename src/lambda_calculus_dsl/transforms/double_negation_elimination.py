from dataclasses import dataclass
from typing import Any
from .transform import dummy_transform


@dataclass
class Keep:
    value: Any


@dataclass
class Negate:
    value: Any


def fwd(x):
    return Keep(value=x)


def bwd(x):
    if isinstance(x, Keep):
        return x.value
    elif isinstance(x, Negate):
        return lambda s: s.neg(x.value(s))
    raise AssertionError()


class T(dummy_transform(fwd, bwd)):
    @staticmethod
    def neg(x):
        if isinstance(x, Keep):
            return Negate(x.value)
        elif isinstance(x, Negate):
            return Keep(x.value)
        raise AssertionError()


def double_neg_elimination(x):
    return bwd(x(T))
