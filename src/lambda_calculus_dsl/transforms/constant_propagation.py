from ..base.base import App, Builtin, Lit, Var
from ..higher_order.higher_order import Lam
from .transform import as_builtin_call, make_builtin_call, Transform


class UpdateFreeVariables(Transform):
    def visit_Var(self, expr: Var, *, bound=-1, update):
        if expr.idx > bound:
            return Var(update(expr.idx))
        return expr

    def visit_Lam(self, expr: Lam, *, bound=-1, update):
        return self.generic_visit(expr, bound=bound + 1, update=update)


class BetaReduction(Transform):
    def visit_Var(self, expr: Var, *, bound=-1, arg=None):
        if expr.idx == bound:
            return UpdateFreeVariables.apply(arg, update=lambda x: x + bound)
        if expr.idx > bound:
            return Var(expr.idx - 1)
        return expr

    def visit_Lam(self, expr: Lam, *, bound=-1, arg=None):
        return self.generic_visit(expr, bound=bound + 1, arg=arg)

    def visit_App(self, expr: App, *, bound=-1, arg=None):
        if isinstance(expr.fun, Lam) and bound < 0:
            return self.visit(expr.fun.fun, bound=0, arg=expr.arg)
        return self.generic_visit(expr, bound=bound, arg=arg)


class T(Transform):
    def visit_App(self, expr: App):
        expr = self.generic_visit(expr)

        def two_lits(args):
            return (
                isinstance(args, tuple)
                and len(args) == 2
                and all(isinstance(arg, Lit) for arg in args)
            )

        if (x := as_builtin_call(expr, "neg")) and isinstance(x, Lit):
            return Lit(-x.val)
        if (args := as_builtin_call(expr, "add")) and two_lits(args):
            x, y = args
            return Lit(x.val + y.val)
        if (args := as_builtin_call(expr, "mul")) and two_lits(args):
            x, y = args
            return Lit(x.val * y.val)
        if isinstance(expr.fun, Lam):
            return self.visit(BetaReduction.apply(expr))
        return expr


constant_prop = T.apply
