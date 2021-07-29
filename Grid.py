
from Colours import BLACK, WHITE, GREEN, BLUE, RED, YELLOW, PURPLE, LIGHTYELLOW, LIGHTPURPLE
import pygame
from Cell import Cell
import numpy as np

class Grid:
    def __init__(self, gridSize, reactionRates, selectedCoords):
        self.Size = gridSize
        self.Grid = []
        self.GridSquareSize = [20,20] #Size in pixels of each gridsquare
        self.Margin = 1
        self.sources = {'purple':[], 'yellow':[], 'yellowHalf':[], 'purpleHalf':[]}
        self.boundary = {'perm':[], 'full':[]}
        self.selectedCells = []
        self.maxConc = 1.0
        self.halfConc = 0.5
        self.create(reactionRates, selectedCoords)

    def create(self, reactionRates, selectedCoords):

        '''Creating the initial grid matrix'''

        for column in range(self.Size[0]):
            columnVec = []
            for row in range(self.Size[1]):
                newCell = Cell(column, row, reactionRates)
                columnVec.append(newCell)
                if [column, row] in selectedCoords:
                    self.selectedCells.append(newCell)
            self.Grid.append(columnVec)

    def drawGrid(self, display, diffCoeff):

        '''Draw each of the grid squares onto the pygame window,
        including the margin between each of the squares'''

        display.fill(BLACK)
        for column in range(self.Size[0]):
            for row in range(self.Size[1]):
                xpos = (self.Margin + self.GridSquareSize[0])*column + self.Margin
                ypos = (self.Margin + self.GridSquareSize[1])*row + self.Margin
                pygame.draw.rect(display, WHITE, [xpos, ypos, self.GridSquareSize[0], self.GridSquareSize[1]])
        
        for boundary in self.boundary['perm']:
            self.colourGrid(boundary, display, RED)
            self.Grid[boundary[0]][boundary[1]].boundary = diffCoeff['permBoundary']
        for boundary in self.boundary['full']:
            self.colourGrid(boundary, display, GREEN)
            self.Grid[boundary[0]][boundary[1]].boundary = diffCoeff['edgeBoundary']
        for source in self.sources['yellow']:
            self.colourGrid(source, display, YELLOW)
        for source in self.sources['purple']:
            self.colourGrid(source, display, PURPLE)
        for source in self.sources['yellowHalf']:
            self.colourGrid(source, display, LIGHTYELLOW)
        for source in self.sources['purpleHalf']:
            self.colourGrid(source, display, LIGHTPURPLE)

    def colourGrid(self, gridSquare, display, colour):

        '''Used to change the colour of a given grid square coordinate
        does this by drawing over the existing square'''

        xpos = (self.Margin + self.GridSquareSize[0])*gridSquare[0] + self.Margin
        ypos = (self.Margin + self.GridSquareSize[1])*gridSquare[1] + self.Margin
        pygame.draw.rect(display, colour, [xpos, ypos, self.GridSquareSize[0], self.GridSquareSize[1]])

    def boundaryConditions(self, time, test):
        for col in self.Grid:
            for cell in col:
                cell.u1 = np.zeros(time)
                cell.u2 = np.zeros(time)
                cell.u3 = np.zeros(time)
                cell.u4 = np.zeros(time)
                if test:
                    if cell.position in self.sources['yellow']:
                        cell.u1[0] = 0.25
                    if cell.position in self.sources['purple']:
                        cell.u2[0] = 0.75
                else:
                    if cell.position in self.sources['yellow']:
                        cell.u1[0] = self.maxConc
                    if cell.position in self.sources['purple']:
                        cell.u2[0] = self.maxConc
                    if cell.position in self.sources['yellowHalf']:
                        cell.u1[0] = self.halfConc
                    if cell.position in self.sources['purpleHalf']:
                        cell.u2[0] = self.halfConc
        

    def gammaCalculation(self, dt, diffCoeff):
        gamma = [(diffCoeff['yellow'] * dt), (diffCoeff['purple'] * dt), (((diffCoeff['yellow'] + diffCoeff['purple'])/2) * dt), (((diffCoeff['yellow'] + diffCoeff['purple'])/2) * dt)]
        return gamma

    def updateSources(self, test):
        for col in self.Grid:
            for cell in col:
                if (cell.position in self.sources['yellow'] or cell.position in self.sources['purple'] or cell.position in self.sources['yellowHalf'] or cell.position in self.sources['purpleHalf']):
                    if test == False:
                        cell.source = True