
from Colours import BLACK, WHITE, GREEN, BLUE
import pygame

class Grid:
    def __init__(self, gridSize):
        self.Size = gridSize
        self.Grid = []
        self.GridSquareSize = [30,30] #Size in pixels of each gridsquare
        self.Margin = 1
        self.Sources = {'green':[], 'blue':[]}
        self.Boundary = []
        self.create()


    def create(self):

        '''Creating the initial grid matrix'''

        for column in range(self.Size[0]):
            columnVec = []
            for row in range(self.Size[1]):
                columnVec.append([])
            self.Grid.append(columnVec)


    def drawGrid(self, display):

        '''Draw each of the grid squares onto the pygame window,
        including the margin between each of the squares'''

        display.fill(BLACK)
        for column in range(self.Size[0]):
            for row in range(self.Size[1]):
                xpos = (self.Margin + self.GridSquareSize[0])*column + self.Margin
                ypos = (self.Margin + self.GridSquareSize[1])*row + self.Margin
                pygame.draw.rect(display, WHITE, [xpos, ypos, self.GridSquareSize[0], self.GridSquareSize[1]])


    def colourGrid(self, gridSquare, display, colour):

        '''Used to change the colour of a given grid square coordinate
        does this by drawing over the existing square'''

        xpos = (self.Margin + self.GridSquareSize[0])*gridSquare[0] + self.Margin
        ypos = (self.Margin + self.GridSquareSize[1])*gridSquare[1] + self.Margin
        pygame.draw.rect(display, colour, [xpos, ypos, self.GridSquareSize[0], self.GridSquareSize[1]])