from test_main import ex1, ex2, ex3, ex4, ex5, ex6, ex7, ex8, ex9, ex10

from lambda_calculus_dsl import view
from lambda_calculus_dsl.base.base import App, Var
from lambda_calculus_dsl.higher_order.higher_order import Lam
from lambda_calculus_dsl.transforms.constant_propagation import BetaReduction
from lambda_calculus_dsl.transforms.transform import Transform


class T(Transform):
    ...


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


def test_beta_reduction():
    testee = App(Lam(Var(0)), Var(1))
    expected = Var(1)
    assert BetaReduction.apply(testee) == expected

    testee = App(
        Lam(Lam(App(App(Var(3), Var(1)), Lam(App(Var(0), Var(2)))))),
        Lam(App(Var(4), Var(0))),
    )
    expected = Lam(
        App(
            App(Var(2), Lam(App(Var(5), Var(0)))),
            Lam(App(Var(0), Lam(App(Var(6), Var(0))))),
        )
    )
    assert BetaReduction.apply(testee) == expected

    testee = App(
        Lam(Var(1)),
        App(
            Lam(App(App(Var(0), Var(0)), Var(0))),
            Lam(App(App(Var(0), Var(0)), Var(0))),
        ),
    )
    expected = Var(0)
    assert BetaReduction.apply(testee) == expected
