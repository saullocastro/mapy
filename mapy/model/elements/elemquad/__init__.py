import numpy as np
from mapy.model.elements.elem2d import Elem2D
from mapy.reader import user_setattr
from mapy.constants import FLOAT
class IsoQuad(Elem2D):
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
        
    def calc_jacob(self):
        
        
    def calc_k_rs(self, r, s):
        '''
        During numerical integration the stiffness matrix is calculated
        for many points r, s inside the element.
        This function will calculate the k_rs during the numerical integration
        '''
        h1 =  r*(r+1)  * s*(s+1)  / 4.
        h2 = -r*(r-1)  * s*(s+1)  / 4.
        h3 =  r*(r-1)  * s*(s-1)  / 4.
        h4 = -r*(r+1)  * s*(s-1)  / 4.
        h5 = -(r**2-1) * s*(s+1)  / 2.
        h6 = -r*(r-1)  * (s**2-1) / 2.
        h7 = -(r**2-1) * s*(s-1)  / 2.
        h8 = -r*(r+1)  * (s**2-1) / 2.
        h9 = -(r**2-1) * (s**2-1) / 2.
        h  = np.array( [h1, h2, h3, h4, h5, h6, h7, h8, h9], dtype = FLOAT)
        h = h[ :self.ng ]
        #
        h1r =  (2*r+1)  * s*(s+1)  / 4.
        h2r = -(2*r-1)  * s*(s+1)  / 4.
        h3r =  (2*r-1)  * s*(s-1)  / 4.
        h4r = -(2*r+1)  * s*(s-1)  / 4.
        h5r = -2*r      * s*(s+1)  / 2.
        h6r = -(2*r-1)  * (s**2-1) / 2.
        h7r = -2*r      * s*(s-1)  / 2.
        h8r = -(2*r+1)  * (s**2-1) / 2.
        h9r =  2*r      * (s**2-1)
        #
        hr_u = np.array( [h1r,   0, h2r,   0, h3r,   0,
                          h4r,   0, h5r,   0, h6r,   0,
                          h7r,   0, h8r,   0, h9r,   0 ], dtype = FLOAT)
        hr_u = hr_u[ : 2*self.ng ]
        hr_v = np.array( [  0, h1r,   0, h2r,   0, h3r,
                            0, h4r,   0, h5r,   0, h6r,
                            0, h7r,   0, h8r,   0, h9r ], dtype = FLOAT)
        hr_v = hr_v[ : 2*self.ng ]
        #
        h1s =  r*(r+1)  * (2*s+1)  / 4.
        h2s = -r*(r-1)  * (2*s+1)  / 4.
        h3s =  r*(r-1)  * (2*s-1)  / 4.
        h4s = -r*(r+1)  * (2*s-1)  / 4.
        h5s = -(r**2-1) * (2*s+1)  / 2.
        h6s = -r*(r-1)  * 2*s      / 2.
        h7s = -(r**2-1) * (2*s-1)  / 2.
        h8s = -r*(r+1)  * 2*s      / 2.
        h9s =  (r**2-1) * 2*s         
        #
        hs_u = np.array( [h1s,   0, h2s,   0, h3s,   0,
                          h4s,   0, h5s,   0, h6s,   0,
                          h7s,   0, h8s,   0, h9s,   0 ], dtype = FLOAT)
        hs_u = hs_u[ : 2*self.ng ]
        hs_v = np.array( [  0, h1s,   0, h2s,   0, h3s,
                            0, h4s,   0, h5s,   0, h6s,
                            0, h7s,   0, h8s,   0, h9s ], dtype = FLOAT)
        hs_v = hs_v[ : 2*self.ng ]
        #
        dxdr = hr*self.xis
        dxds = hs*self.xis
        dydr = hr*self.yis
        dyds = hs*self.yis
        # 3D case not implemented
        #dzdr = hr*self.zis
        #dzds = hs*self.zis
        #jac_rs = np.array(\
        #    [ [dxdr, dydr, dzdr],
        #      [dxds, dyds, dzds],
        #      [dxdt, dydt, dzdt] ], dtype=FLOAT)
        jac_rs = np.matrix(\
            [ [dxdr, dydr],
              [dxds, dyds] ], dtype=FLOAT)
        det_jac_rs = np.linalg.det( jac_rs )
        jac_inv = jac_rs.getI()
        drdx = jac_inv[0][0]
        dsdx = jac_inv[0][1]
        drdy = jac_inv[1][0]
        dsdy = jac_inv[1][1]
        # considering b for epslon xx, epslon yy and gama xy
        b_rs = np.array(\
               [ drdx * hr_u + dsdx * hs_u,
                 drdy * hr_v + dsdy * hs_v,
                 drdy * hr_u + dsdy * hs_u + drdx * hr_v + dsdx * hs_v ],
                 dtype = FLOAT )
        #TODO calc constitutive matrix
        k_rs = det_jac_rs * np.dot( np.dot( b_rs.transpose(), c ), b_rs )
        return k_rs
        
    def jacobian( self, r, s ):
        #
        

