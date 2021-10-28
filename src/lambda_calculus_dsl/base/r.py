from collections.abc import Callable
from typing import Any

from ..transforms.transform import Transform
from .base import App, Builtin, Lit, Var


class R(Transform):
    def visit_Lit(self, expr: Lit, **kwargs: Any) -> int:
        return expr.val

    def visit_Var(self, expr: Var, *, env: list[int], **kwargs: Any) -> int:
        return env[expr.idx]

    def visit_Builtin(self, expr: Builtin, **kwargs: Any) -> Callable[[int], Any]:
        return {
            "neg": lambda x: -x,
            "add": lambda x: lambda y: x + y,
            "mul": lambda x: lambda y: x * y,
        }[expr.name]

    def visit_App(self, expr: App, **kwargs: Any) -> Any:
        return self.visit(expr.fun, **kwargs)(self.visit(expr.arg, **kwargs))


evaluate = R.apply
