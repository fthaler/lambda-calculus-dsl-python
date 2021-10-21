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
        def f(negate):
            assert not negate
            return x

        return Annotated(kind=Kind.Unknown, value=f)

    def bwd(self, x):
        assert isinstance(x, Annotated)
        return x.value(False)

    def lit(self, x):
        return Annotated(
            kind=Kind.INVERTIBLE,
            value=lambda negate: lambda s: s.lit(-x) if negate else s.lit(x),
        )

    def neg(self, x):
        assert isinstance(x, Annotated) and x.kind == Kind.INVERTIBLE
        return Annotated(kind=Kind.INVERTIBLE, value=lambda negate: x.value(not negate))

    def add(self, x, y):
        assert isinstance(x, Annotated) and x.kind == Kind.INVERTIBLE
        assert isinstance(y, Annotated) and y.kind == Kind.INVERTIBLE
        return Annotated(
            kind=Kind.INVERTIBLE,
            value=lambda negate: lambda s: s.add(
                x.value(negate)(s), y.value(negate)(s)
            ),
        )

    def mul(self, x, y):
        assert isinstance(x, Annotated) and x.kind == Kind.INVERTIBLE
        assert isinstance(y, Annotated) and y.kind == Kind.INVERTIBLE
        return Annotated(
            kind=Kind.INVERTIBLE,
            value=lambda negate: lambda s: s.mul(x.value(negate)(s), y.value(False)(s)),
        )

    def sym(self, x):
        return Annotated(
            kind=Kind.INVERTIBLE,
            value=lambda negate: lambda s: s.neg(s.sym(x)) if negate else s.sym(x),
        )


def push_neg(x):
    t = T()
    return t.bwd(x(t))
