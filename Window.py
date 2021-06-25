from numpy.core.numeric import NaN
from pde import grids
from Colours import WHITE, GREEN, BLUE, BLACK, RED, YELLOW
import pygame
from Model import Model
import tkinter
import math
import sys
import matplotlib.pyplot as plt
import itertools
from DiffusionModel import DiffusionModel
import time
#import testCode

class Window:
    def __init__(self, grid, diffCoeff):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.Grid = grid
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
        if gridSquare in self.Grid.Sources['green']:
            self.Grid.Sources['green'].remove(gridSquare)
            self.Grid.colourGrid(gridSquare, self.screen, WHITE)
        elif gridSquare in self.Grid.Sources['blue']:
            self.Grid.Sources['blue'].remove(gridSquare)
            self.Grid.colourGrid(gridSquare, self.screen, WHITE)
        elif gridSquare in self.Grid.Boundary['perm']:
            self.Grid.Boundary['perm'].remove(gridSquare)
            self.Grid.colourGrid(gridSquare, self.screen, WHITE)
        elif gridSquare in self.Grid.Boundary['full']:
            self.Grid.Boundary['full'].remove(gridSquare)
            self.Grid.colourGrid(gridSquare, self.screen, WHITE)
        else:
            #Adds the grid square to the corresponding source dictionary key
            if self.currentSource == GREEN:
                self.Grid.Sources['green'].append(gridSquare)
            elif self.currentSource == BLUE:
                self.Grid.Sources['blue'].append(gridSquare)
            elif self.currentSource == RED:
                self.Grid.Boundary['perm'].append(gridSquare)
            elif self.currentSource == YELLOW:
                self.Grid.Boundary['full'].append(gridSquare)
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

    def colourGrid(self, dataList, range):

        '''Calculates the correct colours of the grid according to the 
        datalist matrix'''

        #Iterating through each grid square
        for col, arr in enumerate(dataList[0]):
            for row, val in enumerate(arr):
                if [col, row] not in (self.Grid.Boundary['perm'] or self.Grid.Boundary['full']):
                    #Finding the diffusion value and range for each source
                    sourceOne = dataList[0][col][row]
                    sourceTwo = dataList[1][col][row]
                    rangeOne = range[0][1] - range[0][0]
                    rangeTwo = range[1][1] - range[1][0]
                    #Avoiding divide by zero errors
                    if rangeOne == 0:
                        rangeOne = 1
                    if rangeTwo == 0:
                        rangeTwo = 1

                    intensitySourceOne = max(255-(sourceOne/rangeOne*255),0)
                    intensitySourceTwo = max(255-(sourceTwo/rangeTwo*255),0)
                    
                    #Calculating the colour gradient between the two sources
                    colour = (255, intensitySourceOne, intensitySourceTwo)
                if [col, row] in self.Grid.Boundary['perm']:
                    colour = RED
                if [col, row] in self.Grid.Boundary['full']:
                    colour = YELLOW
                self.Grid.colourGrid([col, row], self.screen, colour)


    def runModel(self, time):

        '''Function that performs the diffusion method on the sources'''

        model = Model(self.Grid)
        dataList = []
        testData = []
        #Find the minimum dt, as it needs to be the same for all sources
        dt = min((1/(4*self.diffCoeff['green'])), (1/(4*self.diffCoeff['blue'])))
        #Runs diffusion method for each source type
        diff = DiffusionModel(self.Grid, self.Grid.Sources, self.diffCoeff, dt, [self.diffCoeff['permBoundary'], self.diffCoeff['edgeBoundary']])
        dataList = diff.run(time)
        #testData.append(diff)
        #data = model.diffusion(10)
        #Finds max and min for each source
        mergedDataOne = list(itertools.chain(*dataList[0]))
        mergedDataTwo = list(itertools.chain(*dataList[1]))
        rangeOne = [min(mergedDataOne), max(mergedDataOne)]
        rangeTwo = [min(mergedDataTwo), max(mergedDataTwo)]
        #self.createGraph(data)
        #Recolours the grid accordingly
        self.colourGrid(dataList, [rangeOne, rangeTwo])
        self.Grid.Sources = []
        #Uncomment following line to run test on total concentration
        #testCode.testConcentration(testData)

    def runModelAnimation(self, maxTime, timeInterval):
        frameList = []
        rangeList = []
        dataList = []
        dt = min((1/(4*self.diffCoeff['green'])), (1/(4*self.diffCoeff['blue'])))
        for frame in range(0, maxTime, timeInterval):
            for key, val in self.Grid.Sources.items():
                diff = DiffusionModel(self.Grid, val, self.diffCoeff[key], dt)
                data = diff.run(frame)
                dataList.append(data)
            mergedDataOne = list(itertools.chain(*dataList[0]))
            mergedDataTwo = list(itertools.chain(*dataList[1]))
            rangeOne = [min(mergedDataOne), max(mergedDataOne)]
            rangeTwo = [min(mergedDataTwo), max(mergedDataTwo)]
            rangeList.append([rangeOne, rangeTwo])
            frameList.append(dataList)
        count = 0
        for frame in frameList:
            #print(frame[count], rangeList[count])
            self.colourGrid(frameList[count], rangeList[count])
            pygame.display.update()
            time.sleep(3)
            count += 1
        self.Grid.Sources = []
        

    def buttonPressed(self):

        '''Function that is run once a button has been pressed'''

        mousePosition = pygame.mouse.get_pos()
        for key, val in self.buttons.items():
            if mousePosition[0] in range(round(val[0]), round(val[1])):
                if key == 'black':
                    self.runModel(100)
                    #self.runModelAnimation(100, 10)
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
        self.Grid.drawGrid(self.screen)

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