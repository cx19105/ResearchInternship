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

def getEquations(u1, u2, u3, u4):
    '''
    Function to store all of the reactions for each cell
    Form: [[equation of form aA + bB = cC + dD], Reactants, Products, [a,b,c,d], k]
    '''
    reactions = []

    # A + B -> C
    #reactions.append([['u1','u2','u3', None], [u1, u2], [u3, None], [1,1,2,0], 2])

    # C -> A + B
    #reactions.append([['u3', None, 'u1', 'u2'], [u3, None], [u1, u2], [2,0,0.5, 1.5], 1.5])

    # A -> B
    #reactions.append([['u1', None, 'u2', None], [u1, None], [u2, None], [1, 0, 1, 0], 1])

    '''Michaelis-Menten Kinetics
    u1 = E
    u2 = S
    u3 = P
    u4 = ES
    '''
    reactions.append([['u1', 'u2', 'u4','None'], [u1, u2], [u4, None],[1, 1, 1, 0], 1])
    reactions.append([['u4', None, 'u1', 'u3'], [u4, None], [u1, u3], [1, 0, 1, 1], 1])

    return reactions

def generalEquation(reactants, products, reactionCoeffs, k, u_new):
    '''
    equation: The equation in string form so the sources can be correctly assigned to
    reactants: [conc1, conc2] an array of the two concentrations of the reactants in the equation
    products: [conc3, conc4] the concentration of the outputted chemicals
    reactionCoeffs: [a, b, c, d] the coeffs in the equation aA + bB = cC + dD
    where A,B and C are the products and reactants
    k: rate constant
    '''

    A = reactants[0]
    B = reactants[1]
    C = products[0]
    D = products[1]
    [a,b,c,d] = reactionCoeffs

    x, y = 0.01*a, 0.01*b
    if A != None and B != None:
        v = k * A**x * B**y
    elif A == None:
        v = k*B**y
    else:
        v = k*A**x

    dA = -v*a
    dB = -v*b
    dC = v*c
    dD = v*d
    
    new_u = [dA, dB, dC, dD]

    return new_u
