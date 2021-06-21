from Window import Window
from Grid import Grid
from FileReader import FileReader

GRIDSIZE = (50,50)
DIFFCOEFF = {'green':0.2, 'blue':0.5, 'boundary':0.9}

#Insert filename for grid
filename = 'ResearchInternship/sampleGrid.txt'
gridFile = None

if filename != None:
    gridFile = FileReader(filename)
    grid = Grid(gridFile.getGridSize())
    gridFile.createImage(grid)
else:
    grid = Grid(GRIDSIZE)

window = Window(grid, DIFFCOEFF)

window.updateWindow()