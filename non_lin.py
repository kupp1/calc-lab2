import numpy as np
import math

class NonlinEq:
    def __init__(self, f, d1, d2):
        self.f = f
        self.d1 = d1
        self.d2 = d2

    def solve_by_bisection(self, a, b, eps):
        while abs(a - b) > eps:
            c = (a + b) / 2

            print('%.3f %.3f %.3f %.3f %.3f %.3f %.3f' %
             (a, b, c, self.f(a), self.f(b), self.f(c), abs(a - b)))

            if self.f(a) * self.f(c) < 0:
                b = c
            else:
                a = c

        return c

    def solve_by_newtons(self, x0, eps):
        last_x = x0
        for x in np.linspace(x0 - eps, x0 + eps, 100):
            if self.f(x) * self.d2(x) > 0:
                last_x = x
                break
        
        while True:
            x = last_x - self.f(last_x)/self.d1(last_x)

            print('%.3f %.3f %.3f %.3f %.3f' %
             (last_x, self.f(last_x), self.d1(last_x), x, abs(x - last_x)))

            if abs(x - last_x) <= eps:
                break

            last_x = x

        return x

    def solve_by_simple_iter(self, x0, eps):
        d1_max = -math.inf
        for x in np.linspace(x0 - eps, x0 + eps, 100):
            d1_max = max(d1_max, self.d1(x))
        print(d1_max)
        k = -1 / float(d1_max)

        phi = lambda x: x + k * self.f(x)

        last_x = x0
        while True:
            x = phi(last_x)

            print('%.3f %.3f %.3f %.3f %.3f' %
             (last_x, self.f(last_x), x, phi(x), abs(x - last_x)))

            if abs(x - last_x) <= eps:
                break

            last_x = x

        return x
