from ..symbolic.rv import RV as BaseRV
from .higher_order import HigherOrder


class RV(BaseRV, HigherOrder):
    @staticmethod
    def lam(f):
        def bind(symbol_map):
            return lambda x: f(lambda _: x)(symbol_map)

        return bind

    @staticmethod
    def app(f, x):
        return lambda symbol_map: f(symbol_map)(x(symbol_map))


def evaluate_sym(x, sym_map):
    return x(RV)(sym_map)
