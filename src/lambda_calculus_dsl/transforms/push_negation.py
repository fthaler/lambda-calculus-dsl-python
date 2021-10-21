from dataclasses import dataclass
import enum
from typing import Any

from .transform import Transform


class Kind(enum.Enum):
    UNKNOWN = enum.auto()
    INVERTIBLE = enum.auto()


@dataclass
class Annotated:
    kind: Kind
    value: Any


class T(Transform):
    def fwd(self, x):
        assert not isinstance(x, Annotated)

        def f(negate):
            assert not negate
            return x

        return Annotated(kind=Kind.UNKNOWN, value=f)

    def bwd(self, x):
        assert isinstance(x, Annotated)
        return x.value(False)

    def lit(self, x):
        return Annotated(
            kind=Kind.INVERTIBLE,
            value=lambda negate: lambda s: s.lit(-x) if negate else s.lit(x),
        )

    def neg(self, x):
        if x.kind == Kind.INVERTIBLE:
            return Annotated(
                kind=Kind.INVERTIBLE, value=lambda negate: x.value(not negate)
            )
        return super().neg(x)

    def add(self, x, y):
        if x.kind == y.kind == Kind.INVERTIBLE:
            return Annotated(
                kind=Kind.INVERTIBLE,
                value=lambda negate: lambda s: s.add(
                    x.value(negate)(s), y.value(negate)(s)
                ),
            )
        return super().add(x, y)

    def mul(self, x, y):
        if x.kind == y.kind == Kind.INVERTIBLE:
            return Annotated(
                kind=Kind.INVERTIBLE,
                value=lambda negate: lambda s: s.mul(
                    x.value(negate)(s), y.value(False)(s)
                ),
            )
        return super().mul(x, y)

    def sym(self, x):
        return Annotated(
            kind=Kind.INVERTIBLE,
            value=lambda negate: lambda s: s.neg(s.sym(x)) if negate else s.sym(x),
        )


def push_neg(x):
    t = T()
    return t.bwd(x(t))
