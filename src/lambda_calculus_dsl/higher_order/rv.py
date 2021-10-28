from ..symbolic.rv import RV as BaseRV
from .r import R


class RV(BaseRV, R):
    ...


def evaluate_sym(x, sym_map):
    return RV.apply(x, sym_map=sym_map)
