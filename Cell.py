import numpy as np
from scipy.integrate import odeint


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

    def reactionEq(self, z, t):
        u1 = z[0]
        u2 = z[1]
        #Insert differential equation for reaction
        du1dt = (u1-u2)/2
        du2dt = (u1+u2)/5
        dzdt = [du1dt, du2dt]
        return dzdt

    def reactionUpdate(self, neighbouringCells, time, currentValues):

        u1 = currentValues[0]
        u2 = currentValues[1]

        if u1 > 2*u2:
            z0 = [u1, u2]
            tspan = [time, time+1]
            z = odeint(self.reactionEq, z0, tspan)
            return z[1]
        else:
            return [u1, u2]

    def update(self, neighbouringCells, gamma, time):
        currentValues = [self.u1[time], self.u2[time]]
        currentValues = self.diffusionUpdate(neighbouringCells, gamma, time, currentValues)
        currentValues = self.reactionUpdate(neighbouringCells, time, currentValues)
        self.nextValues = currentValues
