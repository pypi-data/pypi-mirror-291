import copy

import sympy

from copul.families.abstract_copula import AbstractCopula
from copul.sympy_wrapper import SymPyFunctionWrapper


class Mardia(AbstractCopula):
    @property
    def is_symmetric(self) -> bool:
        return True

    theta = sympy.symbols("theta")
    params = [theta]
    intervals = {"theta": sympy.Interval(-1, 1, left_open=False, right_open=False)}

    def __init__(self, **kwargs):
        if "theta" in kwargs:
            self.theta = kwargs["theta"]
            self.params = [param for param in self.params if str(param) != "theta"]
            del kwargs["theta"]
        super().__init__(**kwargs)

    def __call__(self, **kwargs):
        if "theta" in kwargs:
            new_copula = copy.deepcopy(self)
            new_copula.theta = kwargs["theta"]
            new_copula.params = [param for param in new_copula.params if str(param) != "theta"]
            del kwargs["theta"]
            return new_copula.__call__(**kwargs)
        return super().__call__(**kwargs)

    @property
    def is_absolutely_continuous(self) -> bool:
        return self.theta == 0 or self.theta == -1

    @property
    def cdf(self):
        frechet_upper = sympy.Min(self.u, self.v)
        frechet_lower = sympy.Max(self.u + self.v - 1, 0)
        cdf = (
            self.theta**2 * (1 + self.theta) / 2 * frechet_upper
            + (1 - self.theta**2) * self.u * self.v
            + self.theta**2 * (1 - self.theta) / 2 * frechet_lower
        )
        return SymPyFunctionWrapper(cdf)

    @property
    def lambda_L(self):
        return self.theta**2 * (1 + self.theta) / 2

    @property
    def lambda_U(self):
        return self.theta**2 * (1 + self.theta) / 2

    def xi(self):
        return self.theta**4 * (3 * self.theta**2 + 1) / 4

    def rho(self):
        return self.theta**3

    def tau(self):
        return self.theta**3 * (self.theta**2 + 2) / 3
