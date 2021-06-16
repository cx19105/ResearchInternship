import numpy as np
from Grid import Grid
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from numpy.core.fromnumeric import repeat

class DiffusionModel:
    def __init__(self, grid):
        self.L = grid.Size
        self.max_time = 750
        diffusionCoeff = 0.2
        self.dx = 1

        self.dt = (self.dx ** 2)/(4*diffusionCoeff)
        self.gamma = (diffusionCoeff * self.dt) / (self.dx ** 2)
        self.u = np.empty((self.max_time, self.L[0], self.L[1]))
        self.boundaryConditions(grid)

    def boundaryConditions(self, grid):

        u_initial = np.zeros(self.L)
        for source in grid.Sources:
            u_initial[source[0]][source[1]] = 100
        u_top = 0
        u_bottom = 0
        u_left = 0
        u_right = 0

        self.u[0,:,:] = u_initial

        self.u[:, (self.L[0]-1):, :] = u_top
        self.u[:, :, :1] = u_left
        self.u[:,:1,1:] = u_bottom
        self.u[:,:,(self.L[1]-1):] = u_right

    def calculate(self, u):
        for k in range(0, self.max_time-1, 1):
            for i in range(1, self.L[0]-1, self.dx):
                for j in range(1, self.L[1]-1, self.dx):
                    u[k+1, i, j] = self.gamma * (u[k][i+1][j] + u[k][i-1][j] + u[k][i][j+1] + u[k][i][j-1] - 4*u[k][i][j]) + u[k][i][j]

        return u

    def plotheatmap(self, u_k, k):
        plt.clf()
        plt.pcolormesh(u_k, cmap=plt.cm.jet, vmin=0, vmax=100)
        plt.colorbar()

        return plt

    def animate(self, k):
        self.plotheatmap(self.u[k], k)

    def run(self):
        self.u = self.calculate(self.u)
        anim = animation.FuncAnimation(plt.figure(), self.animate, interval=1, frames=self.max_time, repeat=False)
        anim.save("heat_equation_solution.gif")

grid = Grid([50, 50])
grid.Sources = [[1, 1], [48, 49], [25, 31], [1, 2], [1,3], [1,4],[1,5],[1,6],[1,7]]


