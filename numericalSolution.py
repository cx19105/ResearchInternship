import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from numpy.core.fromnumeric import repeat

L = 50
max_time = 750

diffusionCoeff = 2
dx = 1

dt = (dx ** 2)/(4*diffusionCoeff)
gamma = (diffusionCoeff * dt) / (dx ** 2)

u = np.empty((max_time, L, L))

u_initial = np.random.uniform(low = 28.5, high = 55.5, size=(L, L))

u_top = 0
u_bottom = 0
u_left = 0
u_right = 0

u[0,:,:] = u_initial

u[:, (L-1):, :] = u_top
u[:, :, :1] = u_left
u[:,:1,1:] = u_bottom
u[:,:,(L-1):] = u_right

def calculate(u):
    for k in range(0, max_time-1, 1):
        for i in range(1, L-1, dx):
            for j in range(1, L-1, dx):
                u[k+1, i, j] = gamma * (u[k][i+1][j] + u[k][i-1][j] + u[k][i][j+1] + u[k][i][j-1] - 4*u[k][i][j]) + u[k][i][j]

    return u

def plotheatmap(u_k, k):
    plt.clf()
    plt.pcolormesh(u_k, cmap=plt.cm.jet, vmin=0, vmax=100)
    plt.colorbar()

    return plt

u = calculate(u)

def animate(k):
    plotheatmap(u[k], k)

anim = animation.FuncAnimation(plt.figure(), animate, interval=1, frames=max_time, repeat=False)
anim.save("heat_equation_solution.gif")