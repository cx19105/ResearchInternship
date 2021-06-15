from pde import grids
from Colours import WHITE, GREEN
import pygame
from Model import Model
import tkinter
import math
import sys
import matplotlib.pyplot as plt
import itertools
from numericalSolution import DiffusionModel

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
        self.screen.fill(WHITE)
        self.running = False

    def getGridSquare(self):
        mousePosition = pygame.mouse.get_pos()
        column = mousePosition[0] / (self.Grid.GridSquareSize[0]+self.Grid.Margin)
        row = mousePosition[1] / (self.Grid.GridSquareSize[1]+self.Grid.Margin)
        gridSquare = [math.floor(column), math.floor(row)]
        return gridSquare

    def makeSource(self, gridSquare):
        if gridSquare in self.Grid.Sources:
            self.Grid.Sources.remove(gridSquare)
            self.Grid.colourGrid(gridSquare, self.screen, WHITE)
        else:
            self.Grid.Sources.append(gridSquare)
            self.Grid.colourGrid(gridSquare, self.screen, GREEN)

    def createGraph(self, data):
        x = range(0, 40)
        plt.plot(x,data)
        plt.show()

    def runModel(self):
        model = Model(self.Grid)
        
        diff = DiffusionModel(self.Grid)
        diff.run()
        data = model.diffusion()
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


    def updateWindow(self):
        self.Grid.drawGrid(self.screen)
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
                        self.runModel()
            pygame.display.update()