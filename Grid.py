from Colours import BLACK, WHITE
import pygame

class Grid:
    def __init__(self, gridSize):
        self.Size = gridSize
        self.Grid = []
        self.GridSquareSize = [20,20]
        self.Margin = 1
        self.Sources = []
        self.create()



    def create(self):
        for column in range(self.Size[0]):
            self.Grid.append([])

    def drawGrid(self, display):
        display.fill(BLACK)
        for column in range(self.Size[0]):
            xpos = (self.Margin + self.GridSquareSize[0])*column + self.Margin
            ypos = self.Margin
            pygame.draw.rect(display, WHITE, [xpos, ypos, self.GridSquareSize[0], self.GridSquareSize[1]])

    