from ..base.r import R as BaseR
from .higher_order import HigherOrder


class R(BaseR, HigherOrder):
    @staticmethod
    def lam(f):
        return f

    @staticmethod
    def app(f, x):
        return f(x)


def evaluate(x):
    return x(R)
