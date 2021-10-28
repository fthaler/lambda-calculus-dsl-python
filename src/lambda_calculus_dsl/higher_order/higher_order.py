from dataclasses import dataclass

from ..base.base import Expr, var


@dataclass
class Lam(Expr):
    fun: Expr


_counter = None


def lam(fun):
    global _counter
    if _counter is not None:
        _counter += 1
        fun(var(-1))
    else:
        _counter = 0
        fun(var(-1))
        counter = _counter
        _counter = None
        return Lam(fun(var(counter)))
