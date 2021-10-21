from abc import abstractmethod

from ..higher_order.higher_order import HigherOrder
from ..symbolic.symbolic import Symbolic


class Transform(HigherOrder, Symbolic):
    @abstractmethod
    def fwd(self, x):
        ...

    @abstractmethod
    def bwd(self, x):
        ...

    def lit(self, x):
        def ex(s):
            return s.lit(x)

        return self.fwd(ex)

    def neg(self, x):
        def ex(s):
            return s.neg(self.bwd(x)(s))

        return self.fwd(ex)

    def add(self, x, y):
        def ex(s):
            return s.add(self.bwd(x)(s), self.bwd(y)(s))

        return self.fwd(ex)

    def mul(self, x, y):
        def ex(s):
            return s.mul(self.bwd(x)(s), self.bwd(y)(s))

        return self.fwd(ex)

    def sym(self, x):
        def ex(s):
            return s.sym(x)

        return self.fwd(ex)

    def lam(self, f):
        def ex(s):
            return s.lam(lambda x: self.bwd(f(self.fwd(lambda _: x)))(s))

        return self.fwd(ex)

    def app(self, f, x):
        def ex(s):
            return s.app(self.bwd(f)(s), self.bwd(x)(s))

        return self.fwd(ex)
