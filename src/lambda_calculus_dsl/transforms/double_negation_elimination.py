from typing import Any

from ..base.base import App, Expr
from .transform import as_builtin_call, Transform


class T(Transform):
    def visit_App(self, expr: Expr, **kwargs: Any) -> Expr:
        if (x := as_builtin_call(expr, "neg", 1)) and (
            y := as_builtin_call(x, "neg", 1)
        ):
            expr = y
        return self.generic_visit(expr)


double_neg_elimination = T.apply
