def f(u1, u2, rates):
    tot = u1 + u2
    u1_new = u1 + rates[0]*u2
    u2_new = tot - u1_new
    return [u1_new, u2_new]

def g(u1, u2, rates):
    tot = u1 + u2
    u1_new = u1 + 0.1*u2
    u2_new = tot - u1_new
    return [u1_new, u2_new]