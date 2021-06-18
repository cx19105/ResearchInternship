from Window import Window
from Grid import Grid

GRIDSIZE = (50,50)
DIFFCOEFF = {'green':0.1, 'blue':0.5}

grid = Grid(GRIDSIZE)

window = Window(grid, DIFFCOEFF)

window.updateWindow()