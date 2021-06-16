from pde import DiffusionPDE, ScalarField, UnitGrid
import numpy as np


class Model:
    def __init__(self, grid):
        self.Grid = grid
        self.Sources = self.Grid.Sources
        self.Diffusivity = 0.5

    def diffusion(self, time):

        grid = UnitGrid(self.Grid.Size)
        state = ScalarField(grid)
        for count in range(0, len(self.Sources)):
            state.insert(self.Sources[count], 10)

        eq = DiffusionPDE(diffusivity=self.Diffusivity)
        result = eq.solve(state, t_range=time)
        return result.data
