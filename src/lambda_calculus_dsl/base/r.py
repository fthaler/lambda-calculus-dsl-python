from .base import Base


class R(Base):
    @staticmethod
    def lit(x: int) -> int:
        return x

    @staticmethod
    def neg(x: int) -> int:
        return -x

    @staticmethod
    def add(x: int, y: int) -> int:
        return x + y

    @staticmethod
    def mul(x: int, y: int) -> int:
        return x * y


def evaluate(x):
    return x(R)
