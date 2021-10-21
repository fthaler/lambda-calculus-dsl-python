from lambda_calculus_dsl import (
    evaluate,
    evaluate_sym,
    view,
    double_neg_elimination,
    push_neg,
    constant_prop,
)


def ex1(s):
    return s.add(s.lit(1), s.lit(2))


def ex2(s):
    return s.sub(s.lit(1), s.lit(2))


def ex3(s):
    return s.sub(s.mul(s.lit(1), s.lit(2)), s.lit(3))


def ex4(s):
    return s.add(s.lit(1), s.sym("x"))


def ex5(s):
    return s.add(s.lit(1), s.mul(s.sym("x"), s.sym("y")))


def ex6(s):
    return s.neg(s.sub(s.mul(s.lit(1), s.lit(2)), s.sym("x")))


def ex7(s):
    return s.neg(s.sub(s.mul(s.lit(1), s.lit(2)), s.neg(s.sym("x"))))


def ex8(s):
    return s.app(s.lam(lambda x: s.add(s.lit(1), x)), s.lit(2))


def ex9(s):
    return s.app(s.lam(lambda x: s.add(ex7(s), x)), s.sym("z"))


def ex10(s):
    return s.lam(lambda x: s.mul(x, s.lit(2)))


def sym_map(x):
    return {"x": 42, "y": -42, "z": 0}[x]


def test_evaluate():
    assert evaluate(ex1) == 3
    assert evaluate(ex2) == -1
    assert evaluate(ex3) == -1
    assert evaluate(ex8) == 3
    assert evaluate(ex10)(1) == 2


def test_evaluate_sym():
    assert evaluate_sym(lambda s: s.sym("x"), sym_map) == 42
    assert evaluate_sym(lambda s: s.sym("y"), sym_map) == -42
    assert evaluate_sym(lambda s: s.sym("z"), sym_map) == 0
    assert evaluate_sym(ex1, sym_map) == 3
    assert evaluate_sym(ex2, sym_map) == -1
    assert evaluate_sym(ex3, sym_map) == -1
    assert evaluate_sym(ex4, sym_map) == 43
    assert evaluate_sym(ex5, sym_map) == -1763
    assert evaluate_sym(ex6, sym_map) == 40
    assert evaluate_sym(ex7, sym_map) == -44
    assert evaluate_sym(ex8, sym_map) == 3
    assert evaluate_sym(ex9, sym_map) == -44
    assert evaluate_sym(ex10, sym_map)(1) == 2


def test_view():
    assert view(ex1) == "1 + 2"
    assert view(ex2) == "1 + -2"
    assert view(ex3) == "1 * 2 + -3"
    assert view(ex4) == "1 + x"
    assert view(ex5) == "1 + x * y"
    assert view(ex6) == "-(1 * 2 + -x)"
    assert view(ex7) == "-(1 * 2 + --x)"
    assert view(ex8) == "(lambda x0: 1 + x0)(2)"
    assert view(ex9) == "(lambda x0: -(1 * 2 + --x) + x0)(z)"
    assert view(ex10) == "lambda x0: x0 * 2"


def test_double_negation_elimination():
    assert view(double_neg_elimination(lambda s: s.neg(s.neg(s.sym("x"))))) == "x"
    assert view(double_neg_elimination(lambda s: s.add(s.lit(1), s.lit(2)))) == "1 + 2"
    assert view(double_neg_elimination(ex7)) == "-(1 * 2 + x)"
    assert view(double_neg_elimination(ex9)) == "(lambda x0: -(1 * 2 + x) + x0)(z)"
    assert view(double_neg_elimination(ex10)) == "lambda x0: x0 * 2"


def test_push_negation():
    assert view(push_neg(ex6)) == "-1 * 2 + x"
    assert view(push_neg(ex7)) == "-1 * 2 + -x"
    assert view(push_neg(ex10)) == "lambda x0: x0 * 2"


def test_constant_propagation():
    assert view(constant_prop(ex1)) == "3"
    assert view(constant_prop(ex2)) == "-1"
    assert view(constant_prop(ex3)) == "-1"
    assert view(constant_prop(ex4)) == "1 + x"
    assert view(constant_prop(ex5)) == "1 + x * y"
    assert view(constant_prop(ex6)) == "-(2 + -x)"
    assert view(constant_prop(ex7)) == "-(2 + --x)"
    assert view(constant_prop(ex8)) == "3"
    assert view(constant_prop(ex9)) == "-(2 + --x) + z"
    assert view(constant_prop(ex10)) == "lambda x0: x0 * 2"
