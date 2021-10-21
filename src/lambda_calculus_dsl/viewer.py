from .higher_order.higher_order import HigherOrder
from .symbolic.symbolic import Symbolic


def _parenp(p, s):
    return "(" + s + ")" if p else s


class Viewer(HigherOrder, Symbolic):
    @staticmethod
    def lit(x):
        def fmt(_):
            return str(x)

        return fmt

    @staticmethod
    def neg(x):
        def fmt(p):
            return _parenp(p > 3, "-" + x(3))

        return fmt

    @staticmethod
    def add(x, y):
        def fmt(p):
            return _parenp(p > 1, x(1) + " + " + y(1))

        return fmt

    @staticmethod
    def mul(x, y):
        def fmt(p):
            return _parenp(p > 2, x(2) + " * " + y(2))

        return fmt

    @staticmethod
    def sym(x):
        def fmt(_):
            return x

        return fmt

    @staticmethod
    def lam(f):
        body0 = f(lambda _: "DUMMY")(0)
        var = "x" + str(body0.count("lambda"))

        def fmt(p):
            return _parenp(p > 0, "lambda " + var + ": " + f(lambda _: var)(0))

        return fmt

    @staticmethod
    def app(f, x):
        def fmt(p):
            return _parenp(p > 4, f(4) + "(" + x(5) + ")")

        return fmt


def view(x):
    return x(Viewer)(0)
