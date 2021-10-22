from abc import abstractmethod
from typing import Callable

from ..base.base import Base


class Symbolic(Base):
    @abstractmethod
    def sym(self, x):
        ...


def sym(x) -> Callable[[Symbolic], any]:
    def ex(s: Symbolic):
        return s.sym(x)
    return ex
