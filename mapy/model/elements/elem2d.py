import alg3dpy
from mapy.reader import user_setattr
from mapy.model.elements import Elements
class Elem2D(Elements):
    __slots__ = [ 'plane' ]

    def __init__(self):
        super( Elem2D, self ).__init__()
        self.xvec = None
        self.yvec = None
        self.zvec = None
    
    def rebuild(self):
        Elements.rebuild(self)
        self.grids = []
        g1 = self.model.griddict[int(self.g1)]
        g2 = self.model.griddict[int(self.g2)]
        g3 = self.model.griddict[int(self.g3)]
        self.grids = [g1, g2, g3]
        if getattr(self, 'g4', False) <> False:
            g4 = self.model.griddict[int(self.g4)]
            self.grids.append( g4 )
            diag1 = g3 - g1
            diag2 = g2 - g4
            self.xvec = diag1 + diag2
        else:
            self.xvec = alg3dpy.vec2points( g1, g2 )
        for grid in self.grids:
            grid.elements[ self.id ] = self
        self.calc_vecs()
        #self.calc_Rmatrix()
        
    
    def calc_vecs(self):
        #zvec
        # FIXME, for more distorted elements this routine should allow a zvec
        # which is the average of many zvecs getting many triangles connecting a
        # central point to each pair of adjacent vertices, until the whole
        # element is evaluated
        grids = self.grids
        self.plane = alg3dpy.plane3points( grids[0], grids[1], grids[2] )    
        self.zvec  = self.plane.normal
        #yvec
        self.yvec  = alg3dpy.ortvec2vecs( self.zvec, self.xvec )
