from Window import Window
from Grid import Grid

GRIDSIZE = (40,1)

grid = Grid(GRIDSIZE)

window = Window(grid)

while True:
    window.updateWindow()