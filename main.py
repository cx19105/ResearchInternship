from Window import Window
from Grid import Grid
from FileReader import FileReader

GRIDSIZE = (50,50)
DIFFCOEFF = {'green':0.8, 'blue':0.8, 'permBoundary':0.8, 'edgeBoundary':0.0}
TIME = 100
CONTINUOUS_SOURCES = True

animation = True

#Insert filename for grid
filename = 'ResearchInternship/sampleGrid2.txt'
gridFile = None

if filename != None:
    gridFile = FileReader(filename)
    grid = Grid(gridFile.getGridSize())
    gridFile.createImage(grid)
else:
    grid = Grid(GRIDSIZE)

window = Window(grid, DIFFCOEFF, TIME, animation, CONTINUOUS_SOURCES)

window.updateWindow()