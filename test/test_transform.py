from dataclasses import dataclass
from typing import Any

from lambda_calculus_dsl import view
from lambda_calculus_dsl.transforms.transform import dummy_transform

from test_main import ex1, ex2, ex3, ex4, ex5, ex6, ex7, ex8, ex9


@dataclass
class Foo:
    value: Any


def fwd(x):
    return Foo(value=x)


def bwd(x):
    assert isinstance(x, Foo)
    return x.value


class T(dummy_transform(fwd, bwd)):
    ...


def test_dummy_transform():
    assert view(bwd(ex1(T()))) == "1 + 2"
    assert view(bwd(ex2(T()))) == "1 + -2"
    assert view(bwd(ex3(T()))) == "1 * 2 + -3"
    assert view(bwd(ex4(T()))) == "1 + x"
    assert view(bwd(ex5(T()))) == "1 + x * y"
    assert view(bwd(ex6(T()))) == "-(1 * 2 + -x)"
    assert view(bwd(ex7(T()))) == "-(1 * 2 + --x)"
    assert view(bwd(ex8(T()))) == "(lambda x0: 1 + x0)(2)"
    assert view(bwd(ex9(T()))) == "(lambda x0: -(1 * 2 + --x) + x0)(z)"
