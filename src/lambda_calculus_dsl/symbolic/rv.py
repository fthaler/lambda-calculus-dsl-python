from ..base.r import R
from .symbolic import Sym


class RV(R):
    def visit_Sym(self, expr: Sym, *, sym_map, **kwargs):
        return sym_map(expr.name)


def evaluate_sym(x, sym_map):
    return RV.apply(x, sym_map=sym_map)
