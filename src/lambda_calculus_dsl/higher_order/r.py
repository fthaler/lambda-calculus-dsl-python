from ..base.r import R as BaseR
from .higher_order import Lam


class R(BaseR):
    def visit_Lam(self, expr: Lam, *, env=None, **kwargs):
        if env is None:
            env = []
        return lambda x: self.visit(expr.fun, env=[x] + env, **kwargs)


evaluate = R.apply
