from ..transforms.transform import Transform
from .base import App, Builtin, Lit, Var


class R(Transform):
    def visit_Lit(self, expr: Lit, **kwargs):
        return expr.val

    def visit_Var(self, expr: Var, *, env, **kwargs):
        return env[expr.idx]

    def visit_Builtin(self, expr: Builtin, **kwargs):
        return {
            "neg": lambda x: -x,
            "add": lambda x: lambda y: x + y,
            "mul": lambda x: lambda y: x * y,
        }[expr.name]

    def visit_App(self, expr: App, **kwargs):
        return self.visit(expr.fun, **kwargs)(self.visit(expr.arg, **kwargs))


evaluate = R.apply
