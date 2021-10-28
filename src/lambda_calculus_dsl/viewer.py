from .base.base import App, Builtin, Lit, Var
from .higher_order.higher_order import Lam
from .symbolic.symbolic import Sym
from .transforms.transform import Transform, as_builtin_call


@staticmethod
def parenp(p, s):
    return "(" + s + ")" if p else s


class S(Transform):
    def visit_Var(self, expr: Var, p: int = 0):
        return f"x{expr.idx}"

    def visit_Lit(self, expr: Lit, p: int = 0):
        return f"{expr.val}"

    def visit_Sym(self, expr: Sym, p: int = 0):
        return expr.name

    def visit_Lam(self, expr: Lam, p: int = 0):
        v = "x" + str(self.visit(expr.fun).count("lambda"))
        return parenp(p > 0, f"lambda {v}: {self.visit(expr.fun)}")

    def visit_App(self, expr: App, p: int = 0):
        if x := as_builtin_call(expr, "neg"):
            return parenp(p > 3, f"-{self.visit(expr.arg, p=3)}")
        if args := as_builtin_call(expr, "add"):
            x, y = args
            return parenp(
                p > 1,
                f"{self.visit(x, p=1)} + {self.visit(y, p=1)}",
            )
        if args := as_builtin_call(expr, "mul"):
            x, y = args
            return parenp(
                p > 2,
                f"{self.visit(x, p=2)} * {self.visit(y, p=2)}",
            )
        return f"{self.visit(expr.fun, p=4)}({self.visit(expr.arg, p=5)})"


view = S.apply


class DeBrujinS(Transform):
    def visit_Var(self, expr: Var, p: int = 0):
        return f"{expr.idx}"

    def visit_Lit(self, expr: Lit, p: int = 0):
        return f"'{expr.val}'"

    def visit_Sym(self, expr: Sym, p: int = 0):
        return f"'{expr.name}'"

    def visit_Builtin(self, expr: Builtin, p: int = 0):
        return f"'{expr.name}'"

    def visit_Lam(self, expr: Lam, p: int = 0):
        return parenp(p > 0, f"λ {self.visit(expr.fun)}")

    def visit_App(self, expr: App, p: int = 0):
        return parenp(p > 4, f"{self.visit(expr.fun, p=4)} {self.visit(expr.arg, p=5)}")


dbview = DeBrujinS.apply
