from pde import DiffusionPDE, ScalarField, UnitGrid
import numpy as np


class Model:
    def __init__(self, grid):
        self.Grid = grid
        self.Sources = self.Grid.Sources
        self.Diffusivity = 0.5

    def diffusion(self):

        grid = UnitGrid(self.Grid.Size)
        print(grid.cell_coords)
        state = ScalarField(grid)
        for count in range(0, len(self.Sources)):
            state.insert(self.Sources[count], 10)

        eq = DiffusionPDE(diffusivity=self.Diffusivity)
        result = eq.solve(state, t_range=10)
        return result.data
