from non_lin import NonlinEq
from eq_lib import eq_lib

x = eq_lib[1].solve_by_simple_iter(3, 0.01)
print('%.3f' % x)