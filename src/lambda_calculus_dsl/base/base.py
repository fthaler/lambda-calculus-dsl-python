from abc import ABC, abstractmethod


class Base(ABC):
    @abstractmethod
    def lit(self, x):
        ...

    @abstractmethod
    def neg(self, x):
        ...

    @abstractmethod
    def add(self, x, y):
        ...

    @abstractmethod
    def mul(self, x, y):
        ...

    def sub(self, x, y):
        return self.add(x, self.neg(y))
