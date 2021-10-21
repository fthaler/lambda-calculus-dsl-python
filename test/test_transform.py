from dataclasses import dataclass
from typing import Any

from lambda_calculus_dsl import view
from lambda_calculus_dsl.transforms.transform import Transform

from test_main import ex1, ex2, ex3, ex4, ex5, ex6, ex7, ex8, ex9, ex10


@dataclass
class Foo:
    value: Any


class T(Transform):
    def fwd(self, x):
        assert not isinstance(x, Foo)
        return Foo(value=x)

    def bwd(self, x):
        assert isinstance(x, Foo)
        return x.value


def test_dummy_transform():
    assert view(T.apply(ex1)) == "1 + 2"
    assert view(T.apply(ex2)) == "1 + -2"
    assert view(T.apply(ex3)) == "1 * 2 + -3"
    assert view(T.apply(ex4)) == "1 + x"
    assert view(T.apply(ex5)) == "1 + x * y"
    assert view(T.apply(ex6)) == "-(1 * 2 + -x)"
    assert view(T.apply(ex7)) == "-(1 * 2 + --x)"
    assert view(T.apply(ex8)) == "(lambda x0: 1 + x0)(2)"
    assert view(T.apply(ex9)) == "(lambda x0: -(1 * 2 + --x) + x0)(z)"
    assert view(T.apply(ex10)) == "lambda x0: x0 * 2"
