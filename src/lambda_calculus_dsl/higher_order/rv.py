from ..symbolic.rv import RV as BaseRV
from .higher_order import HigherOrder


class RV(BaseRV, HigherOrder):
    def lam(self, f):
        def bind(symbol_map):
            return lambda x: f(lambda _: x)(symbol_map)

        return bind

    def app(self, f, x):
        return lambda symbol_map: f(symbol_map)(x(symbol_map))


def evaluate_sym(x, sym_map):
    return x(RV())(sym_map)
