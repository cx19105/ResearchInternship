from Colours import WHITE, GREEN, BLUE, BLACK, RED, YELLOW
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
    def __init__(self, grid, diffCoeff, time, animation, continuousSources):
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
        self.buttons = {'green':[0, self.windowWidth/5], 'blue':[self.windowWidth/5, 2*self.windowWidth/5], 'red':[2*self.windowWidth/5, 3*self.windowWidth/5], 'yellow':[3*self.windowWidth/5, 4*self.windowWidth/5], 'black':[4*self.windowWidth/5, self.windowWidth]}
        self.screen.fill(WHITE)
        self.currentSource = GREEN #Currently selected button
        self.running = False
        self.animation = animation
        self.continuousSources = continuousSources

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
        if gridSquare in self.Grid.sources['green']:
            self.Grid.Sources['green'].remove(gridSquare)
            self.Grid.colourGrid(gridSquare, self.screen, WHITE)
        elif gridSquare in self.Grid.sources['blue']:
            self.Grid.Sources['blue'].remove(gridSquare)
            self.Grid.colourGrid(gridSquare, self.screen, WHITE)
        elif gridSquare in self.Grid.boundary['perm']:
            self.Grid.Boundary['perm'].remove(gridSquare)
            self.Grid.colourGrid(gridSquare, self.screen, WHITE)
        elif gridSquare in self.Grid.boundary['full']:
            self.Grid.Boundary['full'].remove(gridSquare)
            self.Grid.colourGrid(gridSquare, self.screen, WHITE)
        else:
            #Adds the grid square to the corresponding source dictionary key
            if self.currentSource == GREEN:
                self.Grid.sources['green'].append(gridSquare)
            elif self.currentSource == BLUE:
                self.Grid.sources['blue'].append(gridSquare)
            elif self.currentSource == RED:
                self.Grid.boundary['perm'].append(gridSquare)
            elif self.currentSource == YELLOW:
                self.Grid.boundary['full'].append(gridSquare)
            #Recreate the grid with the updated grid colours
            self.Grid.colourGrid(gridSquare, self.screen, self.currentSource)
        

    def drawButtons(self):

        '''Adds all the buttons from the buttons dict to the window'''

        for key, val in self.buttons.items():
            if key == 'green':
                colour = GREEN
            elif key == 'blue':
                colour = BLUE
            elif key == 'red':
                colour = RED
            elif key == 'yellow':
                colour = YELLOW
            else:
                colour = BLACK
            pygame.draw.rect(self.screen, colour, [val[0], self.windowHeight-self.BottomMargin, val[1]-val[0], self.BottomMargin])


    def createGraph(self, data):

        '''Function used for testing the model'''

        x = range(0, 40)
        plt.plot(x,data)
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

    def colourGrid(self, time):

        '''Calculates the correct colours of the grid according to the 
        datalist matrix'''

        #Iterating through each grid square

        dataList = [[],[]]
        for col in self.Grid.Grid:
            for cell in col:
                dataList[0].append(cell.u1[time])
                dataList[1].append(cell.u2[time])
                #if [col, row] not in (self.Grid.boundary['perm'] or self.Grid.boundary['full']):
                    #Finding the diffusion value and range for each source
                    #Avoiding divide by zero errors

        maxSourceOne = 100
        maxSourceTwo = 100

        rangeOne = max(dataList[0]) - min(dataList[0])
        rangeTwo = max(dataList[1]) - min(dataList[1])
        if rangeOne == 0:
            rangeOne = 1
        if rangeTwo == 0:
            rangeTwo = 1

        for col in self.Grid.Grid:
            for cell in col:
                intensitySourceOne = max(255-255*cell.u1[time]/maxSourceOne,0)
                intensitySourceTwo = max(255-255*cell.u2[time]/maxSourceTwo,0)
            
                    #Calculating the colour gradient between the two sources
                colour = (255, intensitySourceOne, intensitySourceTwo)
                if cell.position in self.Grid.boundary['perm']:
                    colour = RED
                if cell.position in self.Grid.boundary['full']:
                    colour = YELLOW
                self.Grid.colourGrid(cell.position, self.screen, colour)


    def runModel(self, time):

        '''Function that performs the diffusion method on the sources'''

        if self.continuousSources:
            self.Grid.updateSources()

        testDataU1 = np.zeros((time, self.Grid.Size[0], self.Grid.Size[1]))
        testDataU2 = np.zeros((time, self.Grid.Size[0], self.Grid.Size[1]))
        #Find the minimum dt, as it needs to be the same for all sources
        dt = min((1/(4*self.diffCoeff['green'])), (1/(4*self.diffCoeff['blue'])))
        #Runs diffusion method for each source type
        self.Grid.boundaryConditions(time)
        gamma = self.Grid.gammaCalculation(dt, self.diffCoeff)
        for timeStep in range(0, time-1):
            testDataTimeStep = [[],[]]
            for col in self.Grid.Grid:
                for cell in col:
                    neighbouringCells = self.getNeighbouringCells(cell.position, self.Grid.Size)
                    cell.update(neighbouringCells, gamma, timeStep)
            for col in self.Grid.Grid:
                for cell in col:
                    cell.u1[timeStep+1] = cell.nextValues[0]
                    cell.u2[timeStep+1] = cell.nextValues[1]
                    testDataU1[timeStep, self.Grid.Grid.index(col), col.index(cell)] = cell.u1[timeStep]
                    testDataU2[timeStep, self.Grid.Grid.index(col), col.index(cell)] = cell.u2[timeStep]
        
        #Finds max and min for each source
        #Recolours the grid accordingly
        self.colourGrid(self.time)
        self.Grid.sources = []
        #Uncomment following line to run test on total concentration
        testCode.testConcentration([testDataU1, testDataU2])

    def runModelAnimation(self, maxTime, timeInterval):
        frameList = []
        rangeList = []
        dataList = []

        if self.continuousSources:
            self.Grid.updateSources()

        dt = min((1/(4*self.diffCoeff['green'])), (1/(4*self.diffCoeff['blue'])))
        self.Grid.boundaryConditions(maxTime)
        gamma = self.Grid.gammaCalculation(dt, self.diffCoeff)
        for timeStep in range(0, maxTime-1):
            for col in self.Grid.Grid:
                for cell in col:
                    neighbouringCells = self.getNeighbouringCells(cell.position, self.Grid.Size)
                    cell.update(neighbouringCells, gamma, timeStep)
            for col in self.Grid.Grid:
                for cell in col:
                    cell.u1[timeStep+1] = cell.nextValues[0]
                    cell.u2[timeStep+1] = cell.nextValues[1]
        frame = 0
        while frame < maxTime:
            self.colourGrid(frame)
            pygame.display.update()
            time.sleep(0.1)
            if frame >= maxTime-1:
                frame = 0
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
                elif key == 'green':
                    self.currentSource = GREEN
                elif key == 'blue':
                    self.currentSource = BLUE
                elif key == 'red':
                    self.currentSource = RED
                elif key == 'yellow':
                    self.currentSource = YELLOW


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