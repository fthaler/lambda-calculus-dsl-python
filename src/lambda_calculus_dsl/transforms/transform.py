from ..higher_order.higher_order import HigherOrder
from ..symbolic.symbolic import Symbolic

def dummy_transform(fwd, bwd):
    class T(HigherOrder, Symbolic):
        @staticmethod
        def lit(x):
            return fwd(lambda s: s.lit(x))

        @staticmethod
        def neg(x):
            return fwd(lambda s: s.neg(bwd(x)(s)))

        @staticmethod 
        def add(x, y):
            return fwd(lambda s: s.add(bwd(x)(s), bwd(y)(s)))

        @staticmethod 
        def mul(x, y):
            return fwd(lambda s: s.mul(bwd(x)(s), bwd(y)(s)))

        @staticmethod
        def sym(x):
            return fwd(lambda s: s.sym(x))

        @staticmethod
        def lam(f):
            return fwd(lambda s: s.lam(lambda x: bwd(f(fwd(lambda _: x)))(s)))

        @staticmethod
        def app(f, x):
            return fwd(lambda s: s.app(bwd(f)(s), bwd(x)(s)))

    return T
