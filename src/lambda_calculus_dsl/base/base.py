class Base:
    @staticmethod
    def lit(x):
        ...

    @staticmethod
    def neg(x):
        ...

    @staticmethod
    def add(x, y):
        ...

    @staticmethod
    def mul(x, y):
        ...

    @classmethod
    def sub(cls, x, y):
        return cls.add(x, cls.neg(y))
