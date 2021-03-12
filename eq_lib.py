from non_lin import NonlinEq

eq_lib = []

eq_lib.append(NonlinEq(
    lambda x: x**3 + 4.81*x**2 - 17.37*x + 5.38,
    [
        lambda x: 3*x**2 + 9.62*x - 17.37,
        lambda x: 6*x + 9.62
    ]
))