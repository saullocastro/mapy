import alg3dpy
from mapy.model.elements.elem1d import Elem1D
from mapy.reader import user_setattr
#
class ElemBar(Elem1D):

    def __init__(self, inputs):
        Elem1D.__init__(self)
        self = user_setattr(self, inputs)

    def rebuild(self):
        Elem1D.rebuild(self)
        self.calc_ovec()
        self.calc_vecs()
        self.calc_Rmatrix()
        self.build_kelem()
    
    def calc_ovec(self):
        if self.x2 == '' or self.x3 == '':
            gref = self.model.griddict[int(self.x1)]
            self.ovec = alg3dpy.Vec([(gref.x1 - self.grids[0].x1), \
                                     (gref.x2 - self.grids[0].x2), \
                                     (gref.x3 - self.grids[0].x3)])
        else:
            self.ovec = alg3dpy.Vec(self.x1, self.x2, self.x3)
   
    def test_build_kelem(self):
        return
        #
        #FIXME these k below are valid for rectangular sections only
        x1 = 0.
        x2 = self.L
        A   = self.pobj.a
        C = self.pobj.C
        E   = self.pobj.matobj.e
        G   = self.pobj.G
        Izz = self.pobj.i1
        Iyy = self.pobj.i2
        #truss terms
        kelem = scipy.ones((12,12))
        #FIXME  change this pts... take from the gauss_legendre.py module
        pts = [0.]
        for r in pts:
            h1 = (1-r)/2.
            h1r = -1/2.
            h2 = (1+r)/2.
            h2r = 1/2.
            J  = x2/2.  #h1r*x1 + h2r*x2 
            #truss
            Bi = 1./J * scipy.array([\
             [ h1r,0,0,0,0,0,         h2r,0,0,0,0,0      ],  #ex
             [   0,0,0,0,0,0,           0,0,0,0,0,0      ],  #betaxy
             [   0,0,0,0,0,0,           0,0,0,0,0,0      ]]) #betaxz
            kelem += np.dot( np.dot( Bi.transpose(), C ), Bi )*J
            #XY components
#            Hw =        scipy.array([[  0,0,0,0,0,0,      0,0,0,0,0,0 ],
#                                     [  0,h1,0,0,0,0,    0,h2,0,0,0,0 ],
#                                     [  0,0,0,0,0,0,    0,0,0,0,0,0 ]])
            Bi = 1./J * scipy.array([[ h1r,0,0,0,0,0,       h2r,0,0,0,0,0 ],
                                     [ 0,h1r,0,0,0,-h1,   0,h2r,0,0,0,-h2 ],
                                     [ 0,0,h1r,0,h1,0,       0,0,0,0,h2,0 ]])
#            Hb =        scipy.array([[ 0,0,0,0,0,0,       0,0,0,0,0,0 ],
#                                     [  0,0,0,0,0,h1,    0,0,0,0,0,h2 ],
#                                     [ 0,0,0,0,0,0,       0,0,0,0,0,0 ]])
            kelem += E*Izz* np.dot( Bi.transpose(), Bi )*J
#            #XZ component
#            Hw =        scipy.array([[  0,0,0,0,0,0,      0,0,0,0,0,0 ],
#                                     [  0,0,0,0,0,0,    0,0,0,0,0,0 ],
#                                     [  0,0,h1,0,0,0,    0,0,h2,0,0,0 ]])
#            Bw = 1./J * scipy.array([[ 0,0,0,0,0,0,       0,0,0,0,0,0 ],
#                                     [ 0,0,0,0,0,0,       0,0,0,0,0,0 ],
#                                     [ 0,0,h1r,0,0,0,   0,0,h2r,0,0,0 ]])
#            Hb =        scipy.array([[ 0,0,0,0,0,0,       0,0,0,0,0,0 ],
#                                     [ 0,0,0,0,0,0,       0,0,0,0,0,0 ],
#                                     [  0,0,0,0,h1,0,    0,0,0,0,h2,0 ]])
#            Bb = 1./J * scipy.array([[ 0,0,0,0,0,0,       0,0,0,0,0,0 ],
#                                     [ 0,0,0,0,0,0,       0,0,0,0,0,0 ],
#                                     [ 0,0,0,0,h1r,0,   0,0,0,0,h2r,0 ]])
#            kelem += E*Iyy*np.dot( Bb.transpose(), Bb )*J
        print 'E',E
        print 'G',G
        print 'Izz',Izz
        print 'Iyy',Iyy
        
        self.kelem = kelem * 2.

    def build_kelem(self):
        import scipy
        import scipy.sparse as ss
        A = self.A
        E = self.E
        L = self.L
        #truss terms
        data1 = scipy.array([E*A/L,-E*A/L,-E*A/L,E*A/L])
        row1  = scipy.array([    0,     6,     0,    6])
        col1  = scipy.array([    0,     0,     6,    6])
        #bending in plane XY terms
        EI_L = E*self.Izz/self.L
        k1 = 12*EI_L/L**2
        k2 = 6*EI_L/L
        k3 = 4*EI_L
        k4 = 2*EI_L
        data2 = [k1, k2,-k1,k2,k3,-k2,k4,k1,-k2,k3,k2,-k1,-k2,k2,k4,-k2]
        row2  = [ 1,  1,  1, 1, 5,  5, 5, 7,  7,11, 5,  7,  7,11,11, 11]
        col2  = [ 1,  5,  7,11, 5,  7,11, 7, 11,11, 1,  1,  5, 1, 5,  7]
        data1.extend(data2)
        row1.extend(row2)
        col1.extend(col2)
        data = scipy.array( data1, dtype='float64')
        row  = scipy.array(  row1, dtype='int8')
        col  = scipy.array(  col1, dtype='int8')

        self.kelem = ss.coo_matrix( (data, (row, col)), shape=(12,12))

    def calc_out_vecs(self):
        self.out_vecs = {}
        tmp = {}
        for sub in self.model.subcases.values():
            E = self.E
            A = self.A
            L = self.L
            ub = self.displ[sub.id](6)
            ua = self.displ[sub.id](0)
            tmp['axial_stress'] = ( ub - ua ) * (E / L)
            tmp['axial_force'] = A * tmp['axial_stress']
            
            self.out_vecs[sub.id] = tmp
