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
        u1_new = rates[0]*u1
        u2_new = rates[1]*u2
        u3_new = (1-rates[0])*u1 + (1-rates[1])*u2 + u3
    else:
        u1_new = u1
        u2_new = u2
        u3_new = u3
    
    return [u1_new, u2_new, u3_new]

def generalEquation(reactants, product, reactionCoeffs, k, u_new):
    '''
    reactants: [conc1, conc2] an array of the two concentrations of the reactants in the equation
    products: conc3 the concentration of the outputted chemical
    reactionCoeffs: [a, b, c] the coeffs in the equation aA + bB = cC 
    where A,B and C are the products and reactants
    k: rate constant
    '''

    A = reactants[0]
    B = reactants[1]
    C = product
    [a,b,c] = reactionCoeffs

    x, y = 0.01*a, 0.01*b

    v = k * A**x * B**y 
    
    dA = -v*a
    dB = -v*b
    dC = v*c

    u_new[0] += dA
    u_new[1] += dB
    u_new[2] += dC

    for i in range(0, len(u_new)):
        if u_new[i] < 0:
            u_new[i] = 0

    return u_new
