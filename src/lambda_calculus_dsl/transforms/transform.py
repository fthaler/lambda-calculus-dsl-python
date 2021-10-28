from dataclasses import fields

from ..base.base import App, Builtin, Expr


class Transform:
    def generic_visit(self, expr: Expr, **kwargs):
        values = dict()
        changed = False
        for field in fields(expr):
            value = getattr(expr, field.name)
            if isinstance(value, Expr):
                v = self.visit(value, **kwargs)
                if v != value:
                    value = v
                    changed = True
            values[field.name] = value
        if changed:
            return type(expr)(**values)
        return expr

    def visit(self, expr: Expr, **kwargs):
        visit_method = f"visit_{type(expr).__name__}"
        if hasattr(self, visit_method):
            return getattr(self, visit_method)(expr, **kwargs)
        return self.generic_visit(expr, **kwargs)

    @classmethod
    def apply(cls, ex, *args, **kwargs):
        return cls().visit(ex, *args, **kwargs)


def as_builtin_call(x, name):
    if isinstance(x, App):
        if isinstance(x.fun, Builtin) and x.fun.name == name:
            return x.arg
        if (
            isinstance(x.fun, App)
            and isinstance(x.fun.fun, Builtin)
            and x.fun.fun.name == name
        ):
            return (x.fun.arg, x.arg)


def make_builtin_call(name, *args):
    x = Builtin(name)
    for arg in args:
        x = App(x, arg)
    return x
