import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


class Cell:
    def __init__(self, x, y):
        self.position = [x, y]
        self.u1 = []
        self.u2 = []
        self.nextValues = []
        self.boundary = 1

    def diffusionUpdate(self, neighbouringCells, gamma, time, currentValues):
        neighbourSum1 = []
        neighbourSum2 = []
        for neighbour in neighbouringCells:
            if neighbour != None:
                neighbourSum1.append(neighbour.u1[time])
                neighbourSum2.append(neighbour.u2[time])
        u1 = gamma[0] * (sum(neighbourSum1) - 4*currentValues[0]) + currentValues[0]
        u2 = gamma[1] * (sum(neighbourSum2) - 4*currentValues[1]) + currentValues[1]

        u1 *= self.boundary
        u2 *= self.boundary

        return [u1, u2]

    def ode_FE(self, f, g, U_0, dt, T):
        '''
        Forward euler method for solving ODE for reaction term
        '''
        N_t = int(round(float(T)/dt))
        u1 = np.zeros(N_t + 1)
        u2 = np.zeros(N_t + 1)
        t = np.linspace(0, N_t * dt, len(u1))
        u1[0] = U_0[0]
        u2[0] = U_0[1]
        for n in range(N_t):
            u1[n+1] = u1[n] + dt*f(u1[n], u2[n], t[n])
            #u2[n+1] = u2[n] + dt*g(u1[n], u2[n], t[n])
        return u1, u2, t

    def reactionEq(self, z):
        u1 = z[0]
        u2 = z[1]
        #Insert differential equation for reaction
        #Initially using u1 + u2 = 2u1

        def f(u1, u2, t):
            return -0.4*u1 + u2

        def g(u1, u2, t):
            return u2

        u1, u2, t = self.ode_FE(f=f, g=g, U_0 = z, dt=0.1, T=11)

        return [u1[-1], u2[-1]]
        #Fraction of chemicals


    def reactionUpdate(self, neighbouringCells, time, currentValues):

        u1 = currentValues[0]
        u2 = currentValues[1]
        z0 = [u1, u2]
        z = self.reactionEq(z0)
        return z

    def update(self, neighbouringCells, gamma, time):
        currentValues = [self.u1[time], self.u2[time]]
        currentValues = self.diffusionUpdate(neighbouringCells, gamma, time, currentValues)
        #currentValues = self.reactionUpdate(neighbouringCells, time, currentValues)
        self.nextValues = currentValues
