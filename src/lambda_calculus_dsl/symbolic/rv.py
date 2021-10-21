from ..base.r import R
from .symbolic import Symbolic


class RV(R, Symbolic):
    def lit(self, x: int):
        def bind(_):
            return x

        return bind

    def neg(self, x):
        def bind(symbol_map):
            return -x(symbol_map)

        return bind

    def add(self, x, y):
        def bind(symbol_map):
            return x(symbol_map) + y(symbol_map)

        return bind

    def mul(self, x, y):
        def bind(symbol_map):
            return x(symbol_map) * y(symbol_map)

        return bind

    def sym(self, x):
        def bind(symbol_map):
            return symbol_map(x)

        return bind


def evaluate_sym(x, sym_map):
    return x(RV())(sym_map)
