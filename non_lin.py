import numpy as np
import math

class NonlinEq:
    def __init__(self, f, d1, d2):
        self.f = f
        self.d1 = d1
        self.d2 = d2

    def solve_by_bisection(self, a, b, eps):
        if self.f(a) * self.f(b) > 0:
            raise ValueError('Метод не сходится: разные знаки на концах отрезка')

        k = 0
        c = (a + b) / 2
        while abs(self.f(c)) > eps:
            k += 1
            c = (a + b) / 2

            #print('%.3f %.3f %.3f %.3f %.3f %.3f %.3f' %
            # (a, b, c, self.f(a), self.f(b), self.f(c), abs(a - b)))

            if self.f(a) * self.f(c) < 0:
                b = c
            else:
                a = c

        d = {}
        d['x'] = float(c)
        d['f(x)'] = self.f(float(c))
        d['k'] = k

        return d

    def solve_by_newtons(self, a, b, eps):
        if self.f(a) * self.f(b) > 0:
            raise ValueError('Метод не сходится: разные знаки на концах отрезка')

        last_x = a;
        for x in np.linspace(a, b + eps, int((b - a) / eps)):
            if self.d1(last_x) * self.d1(x) < 0:
                raise ValueError('Метод не сходится: 1-я производная меняет знак')
            elif self.d2(last_x) * self.d2(x) < 0:
                raise ValueError('Метод не сходится: 2-я производная меняет знак')
            last_x = x

        x0 = 0
        for x0_tmp in [a, b]:
            if self.f(x0_tmp) * self.d2(x0_tmp) > 0:
                x0 = x0_tmp
                break
        else:
            raise ValueError('Метод не сходится')
        
        last_x = x0
        k = 0
        while True:
            k += 1
            x = last_x - self.f(last_x)/self.d1(last_x)

            #print('%.3f %.3f %.3f %.3f %.3f' %
            # (last_x, self.f(last_x), self.d1(last_x), x, abs(x - last_x)))

            if abs(x - last_x) <= eps:
                break

            last_x = x

            if k >= 1000:
                raise ValueError('Метод не сходится')

        d = {}
        d['x'] = float(x)
        d['f(x)'] = self.f(float(x))
        d['k'] = k

        return d

    def solve_by_simple_iter(self, x0, eps):
        k = 1 / self.d1(x0)

        phi = lambda x: x - k * self.f(x)

        last_x = x0
        i = 0
        while True:
            i += 1
            x = phi(last_x)

            #print('%.3f %.3f %.3f %.3f %.3f' %
            # (last_x, self.f(last_x), x, phi(x), abs(x - last_x)))

            if abs(x - last_x) <= eps:
                break

            last_x = x

            if i >= 1000:
                raise ValueError('Метод не сходится')
        return x, i

    def plot_to_figure(self, figure, a, b, eps):
        xs = []
        ys = []

        for x in np.linspace(a, b + eps, int((b - a) / eps)):
            xs.append(x)
            ys.append(self.f(x))

        figure.plot(xs, ys)