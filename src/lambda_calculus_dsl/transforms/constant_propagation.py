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


def bwd(v):
    match v:
        case Unknown(value=x):
            return x
        case Literal(value=x):
            return lambda s: s.lit(x)
        case Function(value=f):
            return lambda s: s.lam(lambda x: bwd(f(fwd(lambda _: x)))(s))
    return x.value(False)


class T(dummy_transform(fwd, bwd)):
    @staticmethod
    def lit(x):
        return Literal(x)

    @staticmethod
    def neg(xv):
        match xv:
            case Literal(value=x):
                return Literal(-x)
            case _:
                return super(T, T).neg(xv)

    @staticmethod
    def add(xv, yv):
        match (xv, yv):
            case (Literal(value=x), Literal(value=y)):
                return Literal(x + y)
            case _:
                return super(T, T).add(xv, yv)

    @staticmethod
    def mul(xv, yv):
        match (xv, yv):
            case (Literal(value=x), Literal(value=y)):
                return Literal(x * y)
            case _:
                return super(T, T).mul(xv, yv)

    @staticmethod
    def lam(f):
        return Function(f)

    @staticmethod
    def app(fv, x):
        match fv:
            case Function(value=f):
                return f(x)
            case _:
                return super(T, T).app(fv, x)


def constant_prop(x):
    return bwd(x(T))
