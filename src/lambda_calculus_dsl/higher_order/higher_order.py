from abc import abstractmethod

from ..base.base import Base


class HigherOrder(Base):
    @abstractmethod
    def lam(self, f):
        ...

    @abstractmethod
    def app(self, f, x):
        ...
