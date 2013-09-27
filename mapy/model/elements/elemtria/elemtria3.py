import numpy as np
#FIXME build the K matrix using Gauss-Legendre numerical integration
#
import alg3dpy
from mapy.model.elements.elem2d import Elem2D
from mapy.reader import user_setattr
class ElemTria3(Elem2D):
    def __init__(self, inputs):
        Elem2D.__init__(self)
        self = user_setattr(self, inputs)
    
    def rebuild(self):
        Elem2D.rebuild(self)
        #self.build_kelem()
    
    def build_kelem(self):     
        import scipy
        C    = self.pobj.C
        t    = self.pobj.t
        #global coords
        x1, x2, x3 = self.grids[0].x1 , self.grids[1].x1 , self.grids[2].x1
        y1, y2, y3 = self.grids[0].x2 , self.grids[1].x2 , self.grids[2].x2
        z1, z2, z3 = self.grids[0].x3 , self.grids[1].x3 , self.grids[2].x3
        #loading coords relative to element plane
        global_coords = scipy.array([\
           [x1, x2, x3],\
           [y1, y2, y3],\
           [z1, z2, z3]], dtype='float32')
        local_coords = np.dot( self.Rcoord2el, global_coords )
        x1, x2, x3 = local_coords[0] 
        y1, y2, y3 = local_coords[1] 
        area = alg3dpy.area_tria( self.grids[0], self.grids[1], self.grids[2] )
        J = 2. * area
        L1x = y2 - y3
        L1y = x3 - x2
        L2x = y3 - y1
        L2y = x1 - x3
        L3x = y1 - y2
        L3y = x2 - x1
        #membrane terms
        B = (1/(2.*area)) * scipy.array(\
            [[  L1x,0,0,0,0,0,    L2x,0,0,0,0,0,      L3x,0,0,0,0,0],
             [  0,L1y,0,0,0,0,    0,L2y,0,0,0,0,      0,L3y,0,0,0,0],
             [L1y,L1x,0,0,0,0,  L2y,L2x,0,0,0,0,    L3y,L3x,0,0,0,0]])
        B_T = B.transpose()
        self.kelem = t*area* np.dot( np.dot( B_T, C ), B )*J
        #bending terms
