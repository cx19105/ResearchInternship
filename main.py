from Window import Window
from Grid import Grid
from FileReader import FileReader
import InitialWindow

entryBoxes = InitialWindow.makeWindow()
test = True

values = {'Gridsize':[int(entryBoxes[0]), int(entryBoxes[1])], 'DiffCoeff':[float(entryBoxes[2]), float(entryBoxes[3]), float(entryBoxes[4]), float(entryBoxes[5])], 'time': int(entryBoxes[6]), 'filename':entryBoxes[7], 
    'toggleSource':entryBoxes[13], 'animation':entryBoxes[14], 'file':entryBoxes[15], 'ReactTerms':[float(entryBoxes[8]), float(entryBoxes[9]), float(entryBoxes[10]), float(entryBoxes[11])], 'timeStep':float(entryBoxes[12])}

GRIDSIZE = values['Gridsize']
DIFFCOEFF = {'purple':values['DiffCoeff'][0], 'yellow':values['DiffCoeff'][1], 'permBoundary':values['DiffCoeff'][2], 'edgeBoundary':values['DiffCoeff'][3]}
REACTTERMS = values['ReactTerms']

TIME = values['time']
CONTINUOUS_SOURCES = values['toggleSource']
animation = values['animation']
TIMESTEP = values['timeStep']

selectedCoords = [[0,0]]

#Insert filename for grid
filename = 'ResearchInternship/'+values['filename']
gridFile = None

if test:
    grid = Grid([1,1], REACTTERMS, selectedCoords)
    grid.sources['yellow'].append([0,0])
    grid.sources['purple'].append([0,0])

elif values['file'] == True:
    gridFile = FileReader(filename)
    grid = Grid(gridFile.getGridSize(), REACTTERMS, selectedCoords)
    gridFile.createImage(grid)

else:
    grid = Grid(GRIDSIZE, REACTTERMS, selectedCoords)

window = Window(grid, DIFFCOEFF, TIME, animation, CONTINUOUS_SOURCES, TIMESTEP, test)

window.updateWindow()