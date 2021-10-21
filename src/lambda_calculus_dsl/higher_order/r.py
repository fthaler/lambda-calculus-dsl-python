from ..base.r import R as BaseR
from .higher_order import HigherOrder


class R(BaseR, HigherOrder):
    def lam(self, f):
        return f

    def app(self, f, x):
        return f(x)


def evaluate(x):
    return x(R())
