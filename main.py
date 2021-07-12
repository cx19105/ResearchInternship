from Window import Window
from Grid import Grid
from FileReader import FileReader
import InitialWindow

entryBoxes = InitialWindow.makeWindow()

values = {'Gridsize':[int(entryBoxes[0]), int(entryBoxes[1])], 'DiffCoeff':[float(entryBoxes[2]), float(entryBoxes[3]), float(entryBoxes[4]), float(entryBoxes[5])], 'time': int(entryBoxes[6]), 'filename':entryBoxes[7], 
    'toggleSource':entryBoxes[12], 'animation':entryBoxes[13], 'file':entryBoxes[14], 'ReactTerms':[float(entryBoxes[8]), float(entryBoxes[9]), float(entryBoxes[10]), float(entryBoxes[11])]}

GRIDSIZE = values['Gridsize']
DIFFCOEFF = {'green':values['DiffCoeff'][0], 'blue':values['DiffCoeff'][1], 'permBoundary':values['DiffCoeff'][2], 'edgeBoundary':values['DiffCoeff'][3]}
REACTTERMS = values['ReactTerms']

TIME = values['time']
CONTINUOUS_SOURCES = values['toggleSource']
animation = values['animation']

selectedCoords = [[10,10],[20,20],[30,30]]

#Insert filename for grid
filename = 'ResearchInternship/'+values['filename']
gridFile = None

if values['file'] == True:
    gridFile = FileReader(filename)
    grid = Grid(gridFile.getGridSize(), REACTTERMS, selectedCoords)
    gridFile.createImage(grid)
else:
    grid = Grid(GRIDSIZE, REACTTERMS, selectedCoords)

window = Window(grid, DIFFCOEFF, TIME, animation, CONTINUOUS_SOURCES)

window.updateWindow()