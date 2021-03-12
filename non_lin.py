import numpy as np

class NonlinEq:
    def __init__(self, f, deriv):
        self.f = f
        self.deriv = deriv

    def solve_by_bisection(self, a, b, eps):
        while abs(a - b) > eps:
            c = (a + b) / 2
            if self.f(a) * self.f(c) < 0:
                b = c
            else:
                a = c

        return c

    def solve_by_newtons(self, a, b, eps):
        lastX = 0
        for x in np.arange(a, b + eps, eps):
            if self.f(x) * self.deriv[1](x) > 0:
                lastX = x
                break
        
    