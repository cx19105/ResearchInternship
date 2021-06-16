from pde import grids
from Colours import WHITE, GREEN, BLUE, BLACK
import pygame
from Model import Model
import tkinter
import math
import sys
import matplotlib.pyplot as plt
import itertools
from DiffusionModel import DiffusionModel

class Window:
    def __init__(self, grid):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.Grid = grid
        self.BottomMargin = 20
        self.windowWidth = (self.Grid.GridSquareSize[0]+self.Grid.Margin)*self.Grid.Size[0] + self.Grid.Margin
        self.windowHeight = (self.Grid.GridSquareSize[1]+self.Grid.Margin)*self.Grid.Size[1] + self.Grid.Margin + self.BottomMargin
        self.screen = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        self.clock = pygame.time.Clock()
        self.buttons = {'green':[0, self.windowWidth/4], 'blue':[self.windowWidth/4, self.windowWidth/2], 'black':[self.windowWidth/2, self.windowWidth]}
        self.screen.fill(WHITE)
        self.currentSource = GREEN
        self.running = False

    def getGridSquare(self):
        mousePosition = pygame.mouse.get_pos()
        column = mousePosition[0] / (self.Grid.GridSquareSize[0]+self.Grid.Margin)
        row = mousePosition[1] / (self.Grid.GridSquareSize[1]+self.Grid.Margin)
        gridSquare = [math.floor(column), math.floor(row)]
        return gridSquare

    def makeSource(self, gridSquare):
        if gridSquare in self.Grid.Sources['green']:
            self.Grid.Sources['green'].remove(gridSquare)
            self.Grid.colourGrid(gridSquare, self.screen, WHITE)
        elif gridSquare in self.Grid.Sources['blue']:
            self.Grid.Sources['blue'].remove(gridSquare)
            self.Grid.colourGrid(gridSquare, self.screen, WHITE)
        else:
            if self.currentSource == GREEN:
                self.Grid.Sources['green'].append(gridSquare)
            elif self.currentSource == BLUE:
                self.Grid.Sources['blue'].append(gridSquare)
            self.Grid.colourGrid(gridSquare, self.screen, self.currentSource)
        

    def drawButtons(self):
        for key, val in self.buttons.items():
            if key == 'green':
                colour = GREEN
            elif key == 'blue':
                colour = BLUE
            else:
                colour = BLACK
            pygame.draw.rect(self.screen, colour, [val[0], self.windowHeight-self.BottomMargin, val[1]-val[0], self.BottomMargin])


    def createGraph(self, data):
        x = range(0, 40)
        plt.plot(x,data)
        plt.show()

    def runModel(self):
        model = Model(self.Grid)
        for key, val in self.Grid.Sources:
            diff = DiffusionModel(self.Grid, val)
            data = diff.run(10)
        #data = model.diffusion(10)

        mergedData = list(itertools.chain(*data))
        maxData = max(mergedData)
        minData = min(mergedData)
        #self.createGraph(data)
        for col, arr in enumerate(data):
            for row, val in enumerate(arr):
                intensity = max(255-(val/(maxData - minData)*255),0)
                colour = (255, intensity, intensity)
                self.Grid.colourGrid([col, row], self.screen, colour)
        self.Grid.Sources = []


    def buttonPressed(self):
        mousePosition = pygame.mouse.get_pos()
        for key, val in self.buttons.items():
            if mousePosition[0] in range(round(val[0]), round(val[1])):
                if key == 'black':
                    self.runModel()
                elif key == 'green':
                    self.currentSource = GREEN
                elif key == 'blue':
                    self.currentSource = BLUE


    def updateWindow(self):
        self.Grid.drawGrid(self.screen)
        self.drawButtons()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if pygame.mouse.get_pressed()[0] == 1:
                    if pygame.mouse.get_pos()[1] < self.windowHeight - self.BottomMargin:
                        gridSquare = self.getGridSquare()
                        self.makeSource(gridSquare)
                    else:
                        self.buttonPressed()
            pygame.display.update()