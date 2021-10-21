from dataclasses import dataclass
from typing import Any

from lambda_calculus_dsl import view
from lambda_calculus_dsl.transforms.transform import Transform

from test_main import ex1, ex2, ex3, ex4, ex5, ex6, ex7, ex8, ex9


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
    t = T()
    assert view(t.bwd(ex1(t))) == "1 + 2"
    assert view(t.bwd(ex2(t))) == "1 + -2"
    assert view(t.bwd(ex3(t))) == "1 * 2 + -3"
    assert view(t.bwd(ex4(t))) == "1 + x"
    assert view(t.bwd(ex5(t))) == "1 + x * y"
    assert view(t.bwd(ex6(t))) == "-(1 * 2 + -x)"
    assert view(t.bwd(ex7(t))) == "-(1 * 2 + --x)"
    assert view(t.bwd(ex8(t))) == "(lambda x0: 1 + x0)(2)"
    assert view(t.bwd(ex9(t))) == "(lambda x0: -(1 * 2 + --x) + x0)(z)"
