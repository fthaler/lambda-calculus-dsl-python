from ..base.r import R
from .symbolic import Symbolic


class RV(R, Symbolic):
    @staticmethod
    def lit(x: int):
        def bind(_):
            return x

        return bind

    @staticmethod
    def neg(x):
        def bind(symbol_map):
            return -x(symbol_map)

        return bind

    @staticmethod
    def add(x, y):
        def bind(symbol_map):
            return x(symbol_map) + y(symbol_map)

        return bind

    @staticmethod
    def mul(x, y):
        def bind(symbol_map):
            return x(symbol_map) * y(symbol_map)

        return bind

    @staticmethod
    def sym(x):
        def bind(symbol_map):
            return symbol_map(x)

        return bind


def evaluate_sym(x, sym_map):
    return x(RV)(sym_map)
