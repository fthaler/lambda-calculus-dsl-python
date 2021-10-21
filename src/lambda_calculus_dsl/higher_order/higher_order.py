from ..base.base import Base


class HigherOrder(Base):
    @staticmethod
    def lam(f):
        ...

    @staticmethod
    def app(f, x):
        ...
