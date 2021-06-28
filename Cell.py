





class Cell:
    def __init__(self, x, y):
        self.position = [x, y]
        self.u1 = []
        self.u2 = []
        self.nextValues = []
        self.boundary = 1

    def diffusionUpdate(self, neighbouringCells, gamma, time):
        neighbourSum1 = []
        neighbourSum2 = []
        for neighbour in neighbouringCells:
            if neighbour != None:
                neighbourSum1.append(neighbour.u1[time])
                neighbourSum2.append(neighbour.u2[time])
        u1 = gamma[0] * (sum(neighbourSum1) - 4*self.u1[time]) + self.u1[time]
        u2 = gamma[1] * (sum(neighbourSum2) - 4*self.u2[time]) + self.u2[time]
        
        u1 *= self.boundary
        u2 *= self.boundary
        
        return [u1, u2]

    def update(self, neighbouringCells, gamma, time):
        self.nextValues = self.diffusionUpdate(neighbouringCells, gamma, time)