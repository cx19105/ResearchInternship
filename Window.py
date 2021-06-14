from Colours import WHITE
import pygame
import tkinter
import math
import sys

class Window:
    def __init__(self, grid):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.Grid = grid
        windowWidth = (self.Grid.GridSquareSize[0]+self.Grid.Margin)*self.Grid.Size[0] + self.Grid.Margin
        windowHeight = (self.Grid.GridSquareSize[1]+self.Grid.Margin)*self.Grid.Size[1] + self.Grid.Margin
        self.screen = pygame.display.set_mode((windowWidth, windowHeight))
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
        else:
            self.Grid.Sources.append(gridSquare)

    def updateWindow(self):

        while True:
            self.Grid.drawGrid(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if pygame.mouse.get_pressed()[0] == 1:
                    gridSquare = self.getGridSquare()
                    self.makeSource(gridSquare)
            pygame.display.update()