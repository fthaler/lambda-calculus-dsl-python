from ..base.base import App, Builtin
from .transform import as_builtin_call, Transform


class T(Transform):
    def visit_App(self, expr: App, **kwargs):
        if (x := as_builtin_call(expr, "neg")) and (y := as_builtin_call(x, "neg")):
            expr = y
        return self.generic_visit(expr)


double_neg_elimination = T.apply
