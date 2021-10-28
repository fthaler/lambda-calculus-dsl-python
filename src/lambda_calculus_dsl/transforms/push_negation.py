from ..base.base import App, Builtin, Lit, Var
from .transform import as_builtin_call, make_builtin_call, Transform


class T(Transform):
    def visit_Lit(self, expr: Lit, *, negate=False):
        if negate:
            return Lit(-expr.val)
        return expr

    def visit_App(self, expr: App, *, negate=False):
        if x := as_builtin_call(expr, "neg"):
            return self.visit(x, negate=not negate)

        if negate:
            if args := as_builtin_call(expr, "add"):
                x, y = args
                return make_builtin_call(
                    "add",
                    self.visit(x, negate=True),
                    self.visit(y, negate=True),
                )
            if args := as_builtin_call(expr, "mul"):
                x, y = args
                return make_builtin_call(
                    "mul",
                    self.visit(x, negate=True),
                    self.visit(y, negate=False),
                )
            assert False

        return self.generic_visit(expr, negate=negate)

    def generic_visit(self, expr, *, negate=False):
        expr = super().generic_visit(expr, negate=False)
        if negate:
            return make_builtin_call("neg", expr)
        return expr


push_neg = T.apply
