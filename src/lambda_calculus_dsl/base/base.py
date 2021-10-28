from dataclasses import dataclass


@dataclass
class Expr:
    ...


@dataclass
class Var(Expr):
    idx: int


@dataclass
class Lit(Expr):
    val: int


@dataclass
class Builtin(Expr):
    name: str


@dataclass
class App(Expr):
    fun: Expr
    arg: Expr


lit = Lit


def neg(x: Expr):
    return App(Builtin("neg"), x)


def add(x: Expr, y: Expr):
    return App(App(Builtin("add"), x), y)


def sub(x: Expr, y: Expr):
    return add(x, neg(y))


def mul(x: Expr, y: Expr):
    return App(App(Builtin("mul"), x), y)


def var(index: int):
    return Var(index)


def app(fun, arg):
    return App(fun, arg)
