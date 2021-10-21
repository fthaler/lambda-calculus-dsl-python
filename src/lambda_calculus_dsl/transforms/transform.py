from ..higher_order.higher_order import HigherOrder
from ..symbolic.symbolic import Symbolic


def dummy_transform(fwd, bwd):
    class T(HigherOrder, Symbolic):
        def lit(self, x):
            return fwd(lambda s: s.lit(x))

        def neg(self, x):
            return fwd(lambda s: s.neg(bwd(x)(s)))

        def add(self, x, y):
            return fwd(lambda s: s.add(bwd(x)(s), bwd(y)(s)))

        def mul(self, x, y):
            return fwd(lambda s: s.mul(bwd(x)(s), bwd(y)(s)))

        def sym(self, x):
            return fwd(lambda s: s.sym(x))

        def lam(self, f):
            return fwd(lambda s: s.lam(lambda x: bwd(f(fwd(lambda _: x)))(s)))

        def app(self, f, x):
            return fwd(lambda s: s.app(bwd(f)(s), bwd(x)(s)))

    return T
