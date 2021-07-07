from Window import Window
from Grid import Grid
from FileReader import FileReader
import InitialWindow

entryBoxes = InitialWindow.makeWindow()

values = {'Gridsize':[int(entryBoxes[0]), int(entryBoxes[1])], 'DiffCoeff':[float(entryBoxes[2]), float(entryBoxes[3]), float(entryBoxes[4]), float(entryBoxes[5])], 'time': int(entryBoxes[6]), 'filename':entryBoxes[7], 
    'toggleSource':entryBoxes[8], 'animation':entryBoxes[9], 'file':entryBoxes[10]}

GRIDSIZE = values['Gridsize']
DIFFCOEFF = {'green':values['DiffCoeff'][0], 'blue':values['DiffCoeff'][1], 'permBoundary':values['DiffCoeff'][2], 'edgeBoundary':values['DiffCoeff'][3]}
TIME = values['time']
CONTINUOUS_SOURCES = values['toggleSource']
animation = values['animation']

#Insert filename for grid
filename = values['filename']
gridFile = None

if values['file'] == True:
    gridFile = FileReader(filename)
    grid = Grid(gridFile.getGridSize())
    gridFile.createImage(grid)
else:
    grid = Grid(GRIDSIZE)

window = Window(grid, DIFFCOEFF, TIME, animation, CONTINUOUS_SOURCES)

window.updateWindow()