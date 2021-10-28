from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Optional

from ..base.base import Expr, var


@dataclass
class Lam(Expr):
    fun: Expr


_counter: Optional[int] = None


def lam(fun: Callable[[Any], Any]) -> Lam:
    global _counter
    if _counter is not None:
        _counter += 1
        fun(var(-1))
        # return garbage to keep mypy happy
        return Lam(var(-1))
    else:
        _counter = 0
        fun(var(-1))
        counter = _counter
        _counter = None
        return Lam(fun(var(counter)))
