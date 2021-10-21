from ..symbolic.rv import RV as BaseRV
from .r import R


class RV(BaseRV, R):
    ...


def evaluate_sym(x, sym_map):
    return x(RV(sym_map))
