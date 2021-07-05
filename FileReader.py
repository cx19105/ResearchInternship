class FileReader:
    def __init__(self, filename):
        self.file = filename
        self.readFile()
        self.boundaryMargin = 10
    
    def readFile(self):

        '''Read the file as a array of each of the rows of the grid'''

        lines = []
        f = open(self.file, "r")
        for line in f:
            lines.append(line.strip('\n'))
        return lines

    def createImage(self, grid):

        '''Updates the grid boundary and sources lists'''
        margin = int(self.boundaryMargin/2)

        fileContent = self.readFile()
        for row, line in enumerate(fileContent):
            for col, cell in enumerate(line):
                if cell == '1':
                    grid.boundary['perm'].append([col+margin, row+margin])
                elif cell == '2':
                    grid.sources['green'].append([col+margin, row+margin])
                elif cell == '3':
                    grid.sources['blue'].append([col+margin, row+margin])
                elif cell == '4':
                    grid.boundary['full'].append([col+margin, row+margin])
    
    def getGridSize(self):

        '''Gets the size of the grid for setting up the grid image'''

        fileContent = self.readFile()
        row = len(fileContent) + self.boundaryMargin
        col = len(fileContent[0]) + self.boundaryMargin
        
        return [col, row]
