def f(u1, u2, u3, rates):
    tot = u1 + u2
    u1_new = u1 + rates[0]*u2
    u2_new = tot - u1_new
    u3_new = u3
    return [u1_new, u2_new, u3_new]

def g(u1, u2, u3, rates):
    tot = u1 + u2
    u1_new = u1 + 0.1*u2
    u2_new = tot - u1_new
    u3_new = u3
    return [u1_new, u2_new, u3_new]

def h(u1, u2, u3, rates):
    tot = u1 + u2 + u3
    if u1 > 10 and u2 > 10:
        u1_new = 0.8*u1
        u2_new = 0.8*u2
        u3_new = 0.2*u1 + 0.2*u2 + u3
    else:
        u1_new = u1
        u2_new = u2
        u3_new = u3
    
    return [u1_new, u2_new, u3_new]