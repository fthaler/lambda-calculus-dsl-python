import sys


def _parenp(p, s):
    return "(" + s + ")" if p else s


def lit(x):
    def fmt(_):
        return str(x)

    return fmt


def neg(x):
    def fmt(p):
        return _parenp(p > 3, "-" + x(3))

    return fmt


def add(x, y):
    def fmt(p):
        return _parenp(p > 1, x(1) + " + " + y(1))

    return fmt


def sub(x, y):
    return add(x, neg(y))


def mul(x, y):
    def fmt(p):
        return _parenp(p > 2, x(2) + " * " + y(2))

    return fmt


def sym(x):
    def fmt(_):
        return x

    return fmt


def lam(f):
    body0 = f(lambda _: "DUMMY")(0)
    var = "x" + str(body0.count("lambda"))

    def fmt(p):
        return _parenp(p > 0, "lambda " + var + ": " + f(lambda _: var)(0))

    return fmt


def app(f, x):
    def fmt(p):
        return _parenp(p > 4, f(4) + "(" + x(5) + ")")

    return fmt


def view(x):
    return x(sys.modules[__name__])(0)
