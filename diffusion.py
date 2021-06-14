from pde import DiffusionPDE, ScalarField, UnitGrid
import numpy as np

def diffusion(initialCoords, initialValues):

    grid = UnitGrid([20,1])
    state = ScalarField(grid)
    for count in range(0, len(initialValues)):
        state.insert(initialCoords[count], 1)

    eq = DiffusionPDE(diffusivity=0.1)
    result = eq.solve(state, t_range=100)
    return result.data

print(diffusion([[3,1]], [1]))