from dataclasses import dataclass

from ..base.base import Expr


@dataclass
class Sym(Expr):
    name: str


def sym(name: str) -> Sym:
    return Sym(name)
