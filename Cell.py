import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import reactionEquations

class Cell:
    def __init__(self, x, y, reactionRates):
        '''
        Cell class contains information about each individual grid square
        '''
        self.position = [x, y]
        self.u1 = []
        self.u2 = []
        self.u3 = []
        self.u4 = []
        self.nextValues = []
        self.boundary = 1
        self.source = False
        self.rates = reactionRates

    def diffusionUpdate(self, neighbouringCells, gamma, time, currentValues):
        '''
        Runs the diffusion code for each cell based on the concentration of the
        cells neighbouring it, which are passed in
        '''
        neighbourSum1 = []
        neighbourSum2 = []
        neighbourSum3 = []
        #neighbourSum4 = []
        for neighbour in neighbouringCells:
            if neighbour != None:
                #Find the concentration in the surrounding cells for each source
                neighbourSum1.append(neighbour.u1[time])
                neighbourSum2.append(neighbour.u2[time])
                neighbourSum3.append(neighbour.u3[time])
                #neighbourSum4.append(neighbour.u4[time])

        #Runs the diffusion numerical method, partial differential equation
        u1 = gamma[0] * (sum(neighbourSum1) - 4*currentValues[0]) + currentValues[0]
        u2 = gamma[1] * (sum(neighbourSum2) - 4*currentValues[1]) + currentValues[1]
        if (sum(neighbourSum3) - 4*currentValues[2]) < 0:
            u3 = currentValues[2]
        else:
            u3 = gamma[2] * (sum(neighbourSum3) - 4*currentValues[2]) + currentValues[2]
        u4 = currentValues[3]

        #Need to update to get better boundary diffusion
        u1 *= self.boundary
        u2 *= self.boundary
        u3 *= self.boundary

        return [u1, u2, u3, u4]

    def reactionUpdate(self, neighbouringCells, time, currentValues):
        '''
        Runs the reaction model for each cell in the grid
        '''
        u1 = currentValues[0]
        u2 = currentValues[1]
        u3 = currentValues[2]
        u4 = currentValues[3]
        
        #Iterates through each reaction equation
        for reaction in reactionEquations.getEquations(u1, u2, u3, u4, self.rates):
            new_u = reactionEquations.generalEquation(reaction[1], reaction[2], reaction[3], reaction[4], currentValues)
            #Updates the correct concentration based on the reaction equation
            for i in range(0, len(new_u)):
                if reaction[0][i] == 'u1':
                    u1 += new_u[i]
                elif reaction[0][i] == 'u2':
                    u2 += new_u[i]
                elif reaction[0][i] == 'u3':
                    u3 += new_u[i]
                elif reaction[0][i] == 'u4':
                    u4 += new_u[i]

        currentValues = [u1, u2, u3, u4]

        for i in range(0, len(currentValues)):
            if currentValues[i] < 0:
                currentValues[i] = 0
        return currentValues

    def update(self, neighbouringCells, gamma, time, test):
        '''
        Update the concentrations of each cell using both the diffusion and
        reaction models
        '''
        #Ensure source's maintain 100 concentration
        if not self.source:
            currentValues = [self.u1[time], self.u2[time], self.u3[time], self.u4[time]]
            
            if test == False:
                #Update diffusion
                currentValues = self.diffusionUpdate(neighbouringCells, gamma, time, currentValues)
            #Update reaction
            currentValues = self.reactionUpdate(neighbouringCells, time, currentValues)
            self.nextValues = currentValues
        else:
            #If cell is a source, maintain the values
            self.nextValues = [self.u1[time], self.u2[time], self.u3[time], self.u4[time]]