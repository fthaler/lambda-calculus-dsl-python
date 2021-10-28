from collections.abc import Callable
from typing import Any, Optional

from ..base.r import R as BaseR
from .higher_order import Lam


class R(BaseR):
    def visit_Lam(self, expr: Lam, *, env: Optional[list[int]]=None, **kwargs: Any) -> Callable[[Any], Any]:
        envl = env if env else []
        return lambda x: self.visit(expr.fun, env=[x] + envl, **kwargs)


evaluate = R.apply
