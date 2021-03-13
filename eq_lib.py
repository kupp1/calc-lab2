from non_lin import NonlinEq
from math import sin, cos

eq_lib = []

eq_lib.append(NonlinEq(
    lambda x: x**3 + 4.81*x**2 - 17.37*x + 5.38,
    lambda x: 3*x**2 + 9.62*x - 17.37,
    lambda x: 6*x + 9.62
))

eq_lib.append(NonlinEq(
    lambda x: 2*sin(3*x) - 4*cos(x/2),
    lambda x: 2 * (sin(x/2) + 3*cos(3*x)),
    lambda x: cos(x/2) - 18*sin(3*x)
))
