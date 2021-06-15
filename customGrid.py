from fipy import CellVariable, Grid2D, Viewer, TransientTerm, DiffusionTerm
from fipy.tools import numerix

nx = 20
ny = nx
dx = 1.
dy = dx
L = dx * nx
mesh = Grid2D(dx=dx, dy=dy, nx=nx, ny=ny)

phi = CellVariable(name = 'solution variable', mesh = mesh, value=0.)

D = 1.
eq = TransientTerm() == DiffusionTerm(coeff=D)

valueTopLeft = 0
valueBottomRight = 1
X, Y = mesh.faceCenters
facesTopLeft = ((mesh.facesLeft & (Y > L / 2))
                | (mesh.facesTop & (X < L / 2)))
facesBottomRight = ((mesh.facesRight & (Y == 1))
                    | (mesh.facesBottom & (X > 18)))

print(facesBottomRight)

phi.constrain(valueTopLeft, facesTopLeft)
phi.constrain(valueBottomRight, facesBottomRight)

if __name__ == '__main__':
    viewer = Viewer(vars = phi, datamin=0., datamax = 1.)
    viewer.plot()
timeStepDuration = 10 * 0.9 * dx**2 / (2 * D)

for step in range(steps):
    eq.solve(var=phi,
             dt=10)
    if __name__ == '__main__':
        viewer.plot()
DiffusionTerm().solve(var=phi)
if __name__ == '__main__':
    while True:
        viewer.plot()