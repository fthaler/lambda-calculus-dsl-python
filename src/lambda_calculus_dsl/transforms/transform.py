from abc import abstractmethod
from toolz.functoolz import compose

from ..base.base import lit, neg, add, mul
from ..higher_order.higher_order import HigherOrder, lam, app
from ..symbolic.symbolic import Symbolic, sym


class Transform(HigherOrder, Symbolic):
    @abstractmethod
    def fwd(self, x):
        ...

    @abstractmethod
    def bwd(self, x):
        ...

    def map1(self, f, x):
        return self.fwd(f(self.bwd(x)))

    def map2(self, f, x, y):
        return self.fwd(f(self.bwd(x), self.bwd(y)))

    def lit(self, x):
        return self.fwd(lit(x))

    def neg(self, x):
        return self.map1(neg, x)

    def add(self, x, y):
        return self.map2(add, x, y)

    def mul(self, x, y):
        return self.map2(mul, x, y)

    def sym(self, x):
        return self.fwd(sym(x))

    def lam(self, f):
        return self.fwd(lam(compose(self.bwd, f, self.fwd)))

    def app(self, f, x):
        return self.map2(app, f, x)

    @classmethod
    def apply(cls, ex, *args, **kwargs):
        t = cls(*args, **kwargs)
        return t.bwd(ex(t))
