from lambda_calculus_dsl import (
    constant_prop,
    double_neg_elimination,
    evaluate,
    evaluate_sym,
    push_neg,
    dbview,
    view,
    add,
    lit,
    sub,
    mul,
    neg,
    sym,
    lam,
    app,
)

ex1 = add(lit(1), lit(2))
ex2 = sub(lit(1), lit(2))
ex3 = sub(mul(lit(1), lit(2)), lit(3))
ex4 = add(lit(1), sym("x"))
ex5 = add(lit(1), mul(sym("x"), sym("y")))
ex6 = neg(sub(mul(lit(1), lit(2)), sym("x")))
ex7 = neg(sub(mul(lit(1), lit(2)), neg(sym("x"))))
ex8 = app(lam(lambda x: add(lit(1), x)), lit(2))
ex9 = app(lam(lambda x: add(ex7, x)), sym("z"))
ex10 = lam(lambda x: mul(x, lit(2)))
ex11 = lam(lambda x: mul(x, x))
ex12 = lam(lambda x: lam(lambda y: add(x, y)))


def sym_map(x):
    return {"x": 42, "y": -42, "z": 0}[x]


def test_evaluate():
    assert evaluate(ex1) == 3
    assert evaluate(ex2) == -1
    assert evaluate(ex3) == -1
    assert evaluate(ex8) == 3
    assert evaluate(ex10)(1) == 2
    assert evaluate(ex11)(2) == 4
    assert evaluate(ex12)(1)(2) == 3


def test_evaluate_sym():
    assert evaluate_sym(sym("x"), sym_map) == 42
    assert evaluate_sym(sym("y"), sym_map) == -42
    assert evaluate_sym(sym("z"), sym_map) == 0
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
    assert evaluate_sym(ex11, sym_map)(2) == 4
    assert evaluate_sym(ex12, sym_map)(1)(2) == 3


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
    assert view(ex11) == "lambda x0: x0 * x0"
    assert view(ex12) == "lambda x1: lambda x0: x1 + x0"


def test_dbview():
    assert dbview(ex1) == "'add' '1' '2'"
    assert dbview(ex2) == "'add' '1' ('neg' '2')"
    assert dbview(ex3) == "'add' ('mul' '1' '2') ('neg' '3')"
    assert dbview(ex4) == "'add' '1' 'x'"
    assert dbview(ex5) == "'add' '1' ('mul' 'x' 'y')"
    assert dbview(ex6) == "'neg' ('add' ('mul' '1' '2') ('neg' 'x'))"
    assert dbview(ex7) == "'neg' ('add' ('mul' '1' '2') ('neg' ('neg' 'x')))"
    assert dbview(ex8) == "(λ 'add' '1' 0) '2'"
    assert (
        dbview(ex9)
        == "(λ 'add' ('neg' ('add' ('mul' '1' '2') ('neg' ('neg' 'x')))) 0) 'z'"
    )
    assert dbview(ex10) == "λ 'mul' 0 '2'"
    assert dbview(ex11) == "λ 'mul' 0 0"
    assert dbview(ex12) == "λ λ 'add' 1 0"


def test_double_negation_elimination():
    assert view(double_neg_elimination(neg(neg(sym("x"))))) == "x"
    assert view(double_neg_elimination(add(lit(1), lit(2)))) == "1 + 2"
    assert view(double_neg_elimination(ex7)) == "-(1 * 2 + x)"
    assert view(double_neg_elimination(ex9)) == "(lambda x0: -(1 * 2 + x) + x0)(z)"
    assert view(double_neg_elimination(ex10)) == "lambda x0: x0 * 2"
    assert view(double_neg_elimination(ex11)) == "lambda x0: x0 * x0"
    assert view(double_neg_elimination(ex12)) == "lambda x1: lambda x0: x1 + x0"


def test_push_negation():
    assert view(push_neg(ex6)) == "-1 * 2 + x"
    assert view(push_neg(ex7)) == "-1 * 2 + -x"
    assert view(push_neg(ex10)) == "lambda x0: x0 * 2"
    assert view(push_neg(ex11)) == "lambda x0: x0 * x0"
    assert view(push_neg(ex12)) == "lambda x1: lambda x0: x1 + x0"


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
    assert view(constant_prop(ex11)) == "lambda x0: x0 * x0"
    assert view(constant_prop(ex12)) == "lambda x1: lambda x0: x1 + x0"


def full_opt(ex):
    return constant_prop(double_neg_elimination(push_neg(ex)))


def test_full_opt():
    assert view(full_opt(ex1)) == "3"
    assert view(full_opt(ex2)) == "-1"
    assert view(full_opt(ex3)) == "-1"
    assert view(full_opt(ex4)) == "1 + x"
    assert view(full_opt(ex5)) == "1 + x * y"
    assert view(full_opt(ex6)) == "-2 + x"
    assert view(full_opt(ex7)) == "-2 + -x"
    assert view(full_opt(ex8)) == "3"
    assert view(full_opt(ex9)) == "-2 + -x + z"
    assert view(full_opt(ex10)) == "lambda x0: x0 * 2"
    assert view(full_opt(ex11)) == "lambda x0: x0 * x0"
    assert view(full_opt(ex12)) == "lambda x1: lambda x0: x1 + x0"
