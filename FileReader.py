class FileReader:
    def __init__(self, filename):
        self.file = filename
        self.readFile()
    
    def readFile(self):

        '''Read the file as a array of each of the rows of the grid'''

        lines = []
        f = open(self.file, "r")
        for line in f:
            lines.append(line.strip('\n'))
        return lines

    def createImage(self, grid):

        '''Updates the grid boundary and sources lists'''

        fileContent = self.readFile()
        for row, line in enumerate(fileContent):
            for col, cell in enumerate(line):
                if cell == '1':
                    grid.Boundary.append([col, row])
                elif cell == '2':
                    grid.Sources['green'].append([col, row])
                elif cell == '3':
                    grid.Sources['blue'].append([col, row])
    
    def getGridSize(self):

        '''Gets the size of the grid for setting up the grid image'''

        fileContent = self.readFile()
        row = len(fileContent)
        col = len(fileContent[0])
        return [col, row]
