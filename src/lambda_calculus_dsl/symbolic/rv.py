from ..base.r import R
from .symbolic import Symbolic


class RV(R, Symbolic):
    def __init__(self, sym_map):
        super().__init__()
        self._sym_map = sym_map

    def sym(self, x):
        return self._sym_map(x)


def evaluate_sym(x, sym_map):
    return x(RV(sym_map))
