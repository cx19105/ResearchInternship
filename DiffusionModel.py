import numpy as np
from Grid import Grid
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from numpy.core.fromnumeric import repeat

class DiffusionModel:

    '''Uses a numerical solution to solve the PDE'''

    def __init__(self, grid, sources, diffusionCoeff, dt, boundaryDiffusion):
        self.Grid = grid
        self.L = self.Grid.Size
        self.max_time = 200
        self.boundaryCoeff = boundaryDiffusion
        self.sources = sources
        self.dt = dt #Time step for the numerical method, fixed for all sources
        self.dx = 1 #Size of each gridSquare
        self.gamma = (diffusionCoeff * self.dt) / (self.dx ** 2)
        self.u = np.empty((self.max_time, self.L[0], self.L[1])) #3D matrix for solution,
        self.boundaryConditions() #Setting boundary conditions

    def boundaryConditions(self):

        u_initial = np.zeros(self.L)
        #Setting each source as an initial condition with value 100
        for source in self.sources:
            u_initial[source[0]][source[1]] = 100
        u_top = 0
        u_bottom = 0
        u_left = 0
        u_right = 0

        self.u[0,:,:] = u_initial
        #Setting the edge conditions
        self.u[:, (self.L[0]-1):, :] = u_top
        self.u[:, :, :1] = u_left
        self.u[:,:1,1:] = u_bottom
        self.u[:,:,(self.L[1]-1):] = u_right

        for boundary in (self.Grid.Boundary['full'] and self.Grid.Boundary['perm']):
            self.u[:, boundary[0], boundary[1]] = 0

    def checkBoundary(self, gridSquare):
        if gridSquare in self.Grid.Boundary['perm']:
            return 'perm'
        elif gridSquare in self.Grid.Boundary['full']:
            return 'edge'
        else:
            return None

    def boundaryDiffusion(self, i, j, k, u):
        if not self.checkBoundary([i+1,j]) in ['perm', 'edge'] and not self.checkBoundary([i-1, j]) in ['perm', 'edge']:
            diff = abs(u[k][i+1][j] - u[k][i-1][j])
            if u[k][i+1][j] < u[k][i-1][j]:
                u[k][i+1][j] = diff*self.boundaryCoeff[0]
            else:
                u[k][i-1][j] = diff*self.boundaryCoeff[0]
        if not self.checkBoundary([i, j+1]) in ['perm', 'edge'] and not self.checkBoundary([i, j-1]) in ['perm', 'edge']:
            diff = abs(u[k][i][j+1] - u[k][i][j-1])
            if u[k][i][j+1] < u[k][i][j-1]:
                u[k][i][j+1] = diff*self.boundaryCoeff[0]
            else:
                u[k][i][j-1] = diff*self.boundaryCoeff[0]
        

    def calculate(self, u):

        '''Function that performs the numerical method
        https://levelup.gitconnected.com/solving-2d-heat-equation-numerically-using-python-3334004aa01a'''
        
        for k in range(0, self.max_time-1, 1):
            for i in range(1, self.L[0]-1, self.dx):
                for j in range(1, self.L[1]-1, self.dx):
                    if self.checkBoundary([i, j]) == None: #Returns true if square is in boundary
                        u[k+1, i, j] = self.gamma * (u[k][i+1][j] + u[k][i-1][j] + u[k][i][j+1] + u[k][i][j-1] - 4*u[k][i][j]) + u[k][i][j]
                    if self.checkBoundary([i, j]) == 'full':
                        u[k+1, i, j] = 0
                    if self.checkBoundary([i, j]) == 'perm':
                        self.boundaryDiffusion(i, j, k, u)
                        u[k+1, i, j] = self.gamma * (u[k][i+1][j] + u[k][i-1][j] + u[k][i][j+1] + u[k][i][j-1] - 4*u[k][i][j]) + u[k][i][j]
        return u

    def plotheatmap(self, u_k, k):
        plt.clf()
        plt.pcolormesh(u_k, cmap=plt.cm.jet, vmin=0, vmax=100)
        plt.colorbar()
        plt.show()

    def run(self, time):

        '''Function that smoothens out the image, by taking
        an average of the consecutive times'''

        self.u = self.calculate(self.u)
        uAtTime = self.u[time, :, :]
        uAhead = self.u[time+1,:,:]
        uBehind = self.u[time-1,:,:]
        mean = np.mean([uAtTime, uAhead, uBehind], axis=0)
        return mean
        #self.plotheatmap(self.u[time], time)



grid = Grid([50, 50])
grid.Sources = [[1, 1], [48, 49], [25, 31], [1, 2], [1,3], [1,4],[1,5],[1,6],[1,7]]


