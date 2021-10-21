from .base import Base


class R(Base):
    def lit(self, x: int) -> int:
        return x

    def neg(self, x: int) -> int:
        return -x

    def add(self, x: int, y: int) -> int:
        return x + y

    def mul(self, x: int, y: int) -> int:
        return x * y


def evaluate(x):
    return x(R())
