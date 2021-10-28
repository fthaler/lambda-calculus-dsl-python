from collections.abc import Callable
from typing import Any, Optional, Union, cast

from ..base.base import App, Expr, Lit, Var
from ..higher_order.higher_order import Lam
from .transform import Transform, as_builtin_call


class UpdateFreeVariables(Transform):
    def visit_Var(
        self, expr: Var, *, bound: int = -1, update: Callable[[int], int]
    ) -> Var:
        if expr.idx > bound:
            return Var(update(expr.idx))
        return expr

    def visit_Lam(
        self, expr: Lam, *, bound: int = -1, update: Callable[[int], int]
    ) -> Lam:
        return self.generic_visit(expr, bound=bound + 1, update=update)


class BetaReduction(Transform):
    def visit_Var(
        self, expr: Var, *, bound: int = -1, arg: Optional[Expr] = None
    ) -> Any:
        if expr.idx == bound:
            assert arg is not None
            return UpdateFreeVariables.apply(arg, update=lambda x: x + bound)
        if expr.idx > bound:
            return Var(expr.idx - 1)
        return expr

    def visit_Lam(
        self, expr: Lam, *, bound: int = -1, arg: Optional[Expr] = None
    ) -> Lam:
        return self.generic_visit(expr, bound=bound + 1, arg=arg)

    def visit_App(
        self, expr: App, *, bound: int = -1, arg: Optional[Expr] = None
    ) -> Any:
        if isinstance(expr.fun, Lam) and bound < 0:
            return self.visit(expr.fun.fun, bound=0, arg=expr.arg)
        return self.generic_visit(expr, bound=bound, arg=arg)


class T(Transform):
    def visit_App(self, expr: App) -> Any:
        expr = self.generic_visit(expr)

        if x := as_builtin_call(expr, "neg", 1):
            if isinstance(x, Lit):
                return Lit(-x.val)
        elif args := as_builtin_call(expr, "add", 2):
            x, y = args
            if isinstance(x, Lit) and isinstance(y, Lit):
                return Lit(x.val + y.val)
        elif args := as_builtin_call(expr, "mul", 2):
            x, y = args
            if isinstance(x, Lit) and isinstance(y, Lit):
                return Lit(x.val * y.val)
        elif isinstance(expr.fun, Lam):
            return self.visit(BetaReduction.apply(expr))
        return expr


constant_prop = T.apply
