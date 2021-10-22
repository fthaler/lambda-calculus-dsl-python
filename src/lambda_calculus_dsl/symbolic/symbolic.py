from abc import abstractmethod
from typing import Any, Callable

from ..base.base import Base


class Symbolic(Base):
    @abstractmethod
    def sym(self, x):
        ...


def sym(x) -> Callable[[Symbolic], Any]:
    def ex(s: Symbolic):
        return s.sym(x)

    return ex
