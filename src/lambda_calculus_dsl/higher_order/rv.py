from collections.abc import Callable
from typing import Any

from ..base.base import Expr
from ..symbolic.rv import RV as BaseRV
from .r import R


class RV(BaseRV, R):
    ...


def evaluate_sym(x: Expr, sym_map: Callable[[str], int]) -> Any:
    return RV.apply(x, sym_map=sym_map)
