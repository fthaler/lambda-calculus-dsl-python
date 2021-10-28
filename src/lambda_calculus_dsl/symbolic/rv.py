from collections.abc import Callable
from typing import Any

from ..base.base import Expr
from ..base.r import R
from .symbolic import Sym


class RV(R):
    def visit_Sym(
        self, expr: Sym, *, sym_map: Callable[[str], int], **kwargs: Any
    ) -> int:
        return sym_map(expr.name)


def evaluate_sym(x: Expr, sym_map: Callable[[str], int]) -> Any:
    return RV.apply(x, sym_map=sym_map)
