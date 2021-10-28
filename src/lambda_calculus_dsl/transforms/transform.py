from dataclasses import fields
from typing import Any, Literal, Optional, TypeVar, Union, overload

from ..base.base import App, Builtin, Expr

T = TypeVar("T", bound=Expr)


class Transform:
    def generic_visit(self, expr: T, **kwargs: Any) -> T:
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
            return type(expr)(**values)  # type: ignore
        return expr

    def visit(self, expr: Expr, **kwargs: Any) -> Any:
        visit_method = f"visit_{type(expr).__name__}"
        if hasattr(self, visit_method):
            return getattr(self, visit_method)(expr, **kwargs)
        return self.generic_visit(expr, **kwargs)

    @classmethod
    def apply(cls, expr: Expr, *args: Any, **kwargs: Any) -> Any:
        return cls().visit(expr, *args, **kwargs)


@overload
def as_builtin_call(expr: Expr, name: str, nargs: Literal[1]) -> Optional[Expr]:
    ...


@overload
def as_builtin_call(
    expr: Expr, name: str, nargs: Literal[2]
) -> Optional[tuple[Expr, Expr]]:
    ...


def as_builtin_call(
    expr: Expr, name: str, nargs: int
) -> Union[None, Expr, tuple[Expr, Expr]]:
    if isinstance(expr, App):
        if isinstance(expr.fun, Builtin) and expr.fun.name == name and nargs == 1:
            return expr.arg
        if (
            isinstance(expr.fun, App)
            and isinstance(expr.fun.fun, Builtin)
            and expr.fun.fun.name == name
            and nargs == 2
        ):
            return (expr.fun.arg, expr.arg)
    return None


def make_builtin_call(name: str, *args: Expr) -> Union[Builtin, App]:
    x: Union[Builtin, App] = Builtin(name)
    for arg in args:
        x = App(x, arg)
    return x
