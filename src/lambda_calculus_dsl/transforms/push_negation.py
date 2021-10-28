from typing import Any

from ..base.base import App, Expr, Lit
from .transform import as_builtin_call, make_builtin_call, Transform


class T(Transform):
    def visit_Lit(self, expr: Lit, *, negate: bool=False) -> Lit:
        if negate:
            return Lit(-expr.val)
        return expr

    def visit_App(self, expr: App, *, negate: bool=False) -> Any:
        if x := as_builtin_call(expr, "neg", 1):
            return self.visit(x, negate=not negate)

        if negate:
            if args := as_builtin_call(expr, "add", 2):
                x, y = args
                return make_builtin_call(
                    "add",
                    self.visit(x, negate=True),
                    self.visit(y, negate=True),
                )
            if args := as_builtin_call(expr, "mul", 2):
                x, y = args
                return make_builtin_call(
                    "mul",
                    self.visit(x, negate=True),
                    self.visit(y, negate=False),
                )
            assert False

        return self.generic_visit(expr, negate=negate)

    def generic_visit(self, expr: Expr, *, negate: bool=False, **kwargs: Any) -> Any:
        expr = super().generic_visit(expr, negate=False, **kwargs)
        if negate:
            return make_builtin_call("neg", expr)
        return expr


push_neg = T.apply
