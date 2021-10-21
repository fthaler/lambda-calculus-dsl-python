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


def bwd(v):
    match v:
        case Keep(value=x):
            return x
        case Negate(value=x):
            return lambda s: s.neg(x(s))
    assert False


class T(dummy_transform(fwd, bwd)):
    @staticmethod
    def neg(v):
        match v:
            case Keep(x):
                return Negate(value=x)
            case Negate(x):
                return Keep(value=x)
        assert False


def double_neg_elimination(x):
    return bwd(x(T))
