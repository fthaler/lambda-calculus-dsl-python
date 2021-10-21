from abc import abstractmethod

from ..base.base import Base


class Symbolic(Base):
    @abstractmethod
    def sym(self, x):
        ...
