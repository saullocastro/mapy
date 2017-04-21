import numpy as np
from mapy.model.elements.elem2d import Elem2D
from mapy.constants import FLOAT

class ElemQuad4(Elem2D):
    '''
    Only membrane components considered up to now
    The bending terms have to be added
    This formulation allows the use of quad elements
    from 4 up to 9 nodes
    '''
    def __init__(self, inputs):
        super( IsoQuad, self ).__init__()
        self.xis = None
        self.yis = None
        self.zis = None
        self.ng = 9

    def rebuild(self):
        xis = np.zeros(9, dtype=FLOAT)
        yis = np.zeros(9, dtype=FLOAT)
        zis = np.zeros(9, dtype=FLOAT)
        for i in range( len(self.grids) ):
            g = self.grids[i]
            xis[i] = g.array[0]
            yis[i] = g.array[1]
            zis[i] = g.array[2]
        self.xis = xis.transpose()
        self.yis = yis.transpose()
        self.zis = zis.transpose()
        self.ng = len(self.grids)



