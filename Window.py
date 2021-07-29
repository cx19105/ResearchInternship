from Colours import WHITE, GREEN, BLUE, BLACK, RED, YELLOW, PURPLE
import pygame
import tkinter
import math
import sys
import testCode
import matplotlib.pyplot as plt
import time
import numpy as np
#import testCode

class Window:
    '''
    Class to hold the grid window along with functions to draw and colour each of the grid squares
    '''
    def __init__(self, grid, diffCoeff, time, animation, continuousSources, timeStep, test, createGraph):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.Grid = grid
        self.time = time
        self.maxTime = time + 1
        self.diffCoeff = diffCoeff  #Dict of diffusion coefficients
        self.BottomMargin = 20
        self.windowWidth = (self.Grid.GridSquareSize[0]+self.Grid.Margin)*self.Grid.Size[0] + self.Grid.Margin
        self.windowHeight = (self.Grid.GridSquareSize[1]+self.Grid.Margin)*self.Grid.Size[1] + self.Grid.Margin + self.BottomMargin
        self.screen = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        #Setting the location and sizes of the buttons
        self.buttons = {'purple':[0, self.windowWidth/5], 'yellow':[self.windowWidth/5, 2*self.windowWidth/5], 'red':[2*self.windowWidth/5, 3*self.windowWidth/5], 'green':[3*self.windowWidth/5, 4*self.windowWidth/5], 'black':[4*self.windowWidth/5, self.windowWidth]}
        self.screen.fill(WHITE)
        self.currentSource = PURPLE #Currently selected button
        self.running = False
        self.animation = animation
        self.continuousSources = continuousSources
        self.selectedCells = []
        self.timeInterval = timeStep
        self.test = test
        self.graph = createGraph

    def getGridSquare(self):

        '''Find the currently clicked on grid square'''

        mousePosition = pygame.mouse.get_pos()
        column = mousePosition[0] / (self.Grid.GridSquareSize[0]+self.Grid.Margin)
        row = mousePosition[1] / (self.Grid.GridSquareSize[1]+self.Grid.Margin)
        gridSquare = [math.floor(column), math.floor(row)]
        return gridSquare

    def makeSource(self, gridSquare):

        '''Function that adds a source to the list if a grid square is clicked'''

        #First checks if the grid square is already a source
        if gridSquare in self.Grid.sources['purple']:
            self.Grid.sources['purple'].remove(gridSquare)
            self.Grid.colourGrid(gridSquare, self.screen, WHITE)
        elif gridSquare in self.Grid.sources['yellow']:
            self.Grid.sources['yellow'].remove(gridSquare)
            self.Grid.colourGrid(gridSquare, self.screen, WHITE)
        elif gridSquare in self.Grid.boundary['perm']:
            self.Grid.boundary['perm'].remove(gridSquare)
            self.Grid.colourGrid(gridSquare, self.screen, WHITE)
        elif gridSquare in self.Grid.boundary['full']:
            self.Grid.boundary['full'].remove(gridSquare)
            self.Grid.colourGrid(gridSquare, self.screen, WHITE)
        else:
            #Adds the grid square to the corresponding source dictionary key
            if self.currentSource == YELLOW:
                self.Grid.sources['yellow'].append(gridSquare)
            elif self.currentSource == PURPLE:
                self.Grid.sources['purple'].append(gridSquare)
            elif self.currentSource == RED:
                self.Grid.boundary['perm'].append(gridSquare)
            elif self.currentSource == GREEN:
                self.Grid.boundary['full'].append(gridSquare)
            #Recreate the grid with the updated grid colours
            self.Grid.colourGrid(gridSquare, self.screen, self.currentSource)
        

    def drawButtons(self):

        '''Adds all the buttons from the buttons dict to the window'''

        for key, val in self.buttons.items():
            if key == 'yellow':
                colour = YELLOW
            elif key == 'purple':
                colour = PURPLE
            elif key == 'red':
                colour = RED
            elif key == 'green':
                colour = GREEN
            else:
                colour = BLACK
            pygame.draw.rect(self.screen, colour, [val[0], self.windowHeight-self.BottomMargin, val[1]-val[0], self.BottomMargin])


    def createGraph(self, cell):

        '''Function used for testing the model'''
        title = 'Concentrations of chemicals in cell: ' + str(cell.position[0])+','+str(cell.position[1])
        timeSpan = range(0, self.maxTime)
        plt.title(title)
        plt.plot(timeSpan, cell.u1, '-r', cell.u2, '-b', cell.u3, '-g', cell.u4, '-k')
        plt.legend(['S', 'E','P', 'ES'])
        plt.show()

    def getNeighbouringCells(self, cellPosition, maxSize):
        #First neighbour is left, then up, right and then down
        neighbours = [None, None, None, None]
        if cellPosition[0] > 0:
            neighbours[0] = (self.Grid.Grid[cellPosition[0] - 1][cellPosition[1]])
        if cellPosition[0] < maxSize[0]-1:
            neighbours[2] = (self.Grid.Grid[cellPosition[0] + 1][cellPosition[1]])
        if cellPosition[1] > 0:
            neighbours[1] = (self.Grid.Grid[cellPosition[0]][cellPosition[1] - 1])
        if cellPosition[1] < maxSize[1]-1:
            neighbours[3] = (self.Grid.Grid[cellPosition[0]][cellPosition[1] + 1])
        return neighbours

    def getValueOfCell(self):
        with open('SelectedCellValues.txt','a') as file:
            file.truncate(0)
            for cell in self.Grid.selectedCells:
                file.write("Cell: "+ str(cell.position)+'\n')
                for time in range(0, len(cell.u1)):
                    file.write(str(time)+': '+ str(cell.u1[time])+' '+str(cell.u2[time])+ ' '+str(cell.u3[time])+'\n')

    def colourGrid(self, time):

        '''Calculates the correct colours of the grid according to the 
        datalist matrix'''

        #Iterating through each grid square

        dataList = [[],[],[]]
        for col in self.Grid.Grid:
            for cell in col:
                dataList[0].append(cell.u1[time])
                dataList[1].append(cell.u2[time])
                dataList[2].append(cell.u3[time])
                #if [col, row] not in (self.Grid.boundary['perm'] or self.Grid.boundary['full']):
                    #Finding the diffusion value and range for each source
                    #Avoiding divide by zero errors

        maxSourceOne = 1
        maxSourceTwo = 1
        maxSourceThree = 1

        rangeOne = max(dataList[0]) - min(dataList[0])
        rangeTwo = max(dataList[1]) - min(dataList[1])
        rangeThree = max(dataList[2]) - min(dataList[2])

        if rangeOne == 0:
            rangeOne = 1
        if rangeTwo == 0:
            rangeTwo = 1
        if rangeThree == 0:
            rangeThree = 1

        for col in self.Grid.Grid:
            for cell in col:
                intensitySourceOne = max(255-255*cell.u1[time]/maxSourceOne,0)
                intensitySourceTwo = max(255-255*cell.u2[time]/maxSourceTwo,0)
                intensitySourceThree = max(255-255*cell.u3[time]/maxSourceThree, 0)
            
                    #Calculating the colour gradient between the two sources
                colour = (intensitySourceThree, intensitySourceTwo, intensitySourceOne)
                if cell.position in self.Grid.boundary['perm']:
                    colour = RED
                if cell.position in self.Grid.boundary['full']:
                    colour = GREEN
                self.Grid.colourGrid(cell.position, self.screen, colour)


    def runModel(self, time):

        '''Function that performs the diffusion method on the sources'''

        if self.continuousSources:
            self.Grid.updateSources(self.test)

        testDataU1 = np.zeros((time, self.Grid.Size[0], self.Grid.Size[1]))
        testDataU2 = np.zeros((time, self.Grid.Size[0], self.Grid.Size[1]))
        testDataU3 = np.zeros((time, self.Grid.Size[0], self.Grid.Size[1]))
        #Find the minimum dt, as it needs to be the same for all sources
        dt = min((1/(4*self.diffCoeff['yellow'])), (1/(4*self.diffCoeff['purple'])))
        #Runs diffusion method for each source type
        self.Grid.boundaryConditions(time, self.test)
        gamma = self.Grid.gammaCalculation(dt, self.diffCoeff)
        for timeStep in range(0, time-1):
            testDataTimeStep = [[],[]]
            for col in self.Grid.Grid:
                for cell in col:
                    neighbouringCells = self.getNeighbouringCells(cell.position, self.Grid.Size)
                    cell.update(neighbouringCells, gamma, timeStep, self.test)
            for col in self.Grid.Grid:
                for cell in col:
                    cell.u1[timeStep+1] = cell.nextValues[0]
                    cell.u2[timeStep+1] = cell.nextValues[1]
                    cell.u3[timeStep+1] = cell.nextValues[2]
                    testDataU1[timeStep, self.Grid.Grid.index(col), col.index(cell)] = cell.u1[timeStep]
                    testDataU2[timeStep, self.Grid.Grid.index(col), col.index(cell)] = cell.u2[timeStep]
                    testDataU3[timeStep, self.Grid.Grid.index(col), col.index(cell)] = cell.u3[timeStep]
        
        #Finds max and min for each source
        #Recolours the grid accordingly
        self.colourGrid(self.time)
        self.Grid.sources = []
        if self.test or self.graph:
            self.createGraph(self.Grid.selectedCells[0])

        #Uncomment following line to run test on total concentration
        #testCode.testConcentration([testDataU1, testDataU2, testDataU3])

    def runModelAnimation(self, maxTime, timeInterval):
        '''
        Runs the model for one time step at a time, then returns each of them as a frame
        to play consecutively as a video animation
        Input the final time and the sleep time between each frame
        '''

        frameList = []
        rangeList = []
        dataList = []

        if self.continuousSources:
            self.Grid.updateSources(self.test)

        dt = min((1/(4*self.diffCoeff['yellow'])), (1/(4*self.diffCoeff['purple'])))
        self.Grid.boundaryConditions(maxTime, self.test)
        gamma = self.Grid.gammaCalculation(dt, self.diffCoeff)
        for timeStep in range(0, maxTime-1):
            for col in self.Grid.Grid:
                for cell in col:
                    neighbouringCells = self.getNeighbouringCells(cell.position, self.Grid.Size)
                    cell.update(neighbouringCells, gamma, timeStep, self.test)
            for col in self.Grid.Grid:
                for cell in col:
                    cell.u1[timeStep+1] = cell.nextValues[0]
                    cell.u2[timeStep+1] = cell.nextValues[1]
                    cell.u3[timeStep+1] = cell.nextValues[2]
                    cell.u4[timeStep+1] = cell.nextValues[3]
        self.getValueOfCell()
        

        frame = 0
        while frame < maxTime:
            self.colourGrid(frame)
            pygame.display.update()
            time.sleep(self.timeInterval)
            if frame >= maxTime-1:
                if self.test == True or self.graph == True:
                    self.createGraph(self.Grid.selectedCells[0])
                    pygame.quit()
                    sys.exit()
            else:
                frame += 1
        
        


    def buttonPressed(self):

        '''Function that is run once a button has been pressed'''

        mousePosition = pygame.mouse.get_pos()
        for key, val in self.buttons.items():
            if mousePosition[0] in range(round(val[0]), round(val[1])):
                if key == 'black':
                    if self.animation == True:
                        self.runModelAnimation(self.maxTime, 10)
                    else:
                        self.runModel(self.maxTime)
                elif key == 'yellow':
                    self.currentSource = YELLOW
                elif key == 'purple':
                    self.currentSource = PURPLE
                elif key == 'red':
                    self.currentSource = RED
                elif key == 'green':
                    self.currentSource = GREEN


    def updateWindow(self):

        '''Function that is run on an infinite loop, checking for updates
        to the window'''

        #Setting up the window
        self.Grid.drawGrid(self.screen, self.diffCoeff)

        self.drawButtons()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                #If the mouse is pressed
                if pygame.mouse.get_pressed()[0] == 1:
                    if pygame.mouse.get_pos()[1] < self.windowHeight - self.BottomMargin:
                        gridSquare = self.getGridSquare()
                        self.makeSource(gridSquare)
                    else:
                        self.buttonPressed()
            pygame.display.update()