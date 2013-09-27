import alg3dpy
class Elements(object):
    
    __slots__ = [ 'id', 'model', 'xvec', 'yvec', 'zvec', 'mask', 'tmp', \
                  'grids', 'cg', 'pobj', 'entryclass', 'card', 'panel' ]

    def __init__(self):
        self.grids = []
        self.mask = False
        self.panel = None

    def rebuild(self):
        if getattr(self, 'pid', False) <> False:
            prop = self.model.propdict[int(self.pid)]
            self.pobj = prop
    
    def calc_cg(self):
        self.cg = alg3dpy.Point( [0,0,0] ) 
        for grid in self.grids:
            self.cg.x1 += grid.x1 
            self.cg.x2 += grid.x2
            self.cg.x3 += grid.x3
        N = len(self.grids)
        self.cg.x1 /= N
        self.cg.x2 /= N 
        self.cg.x3 /= N 

    def add2model(self, model):
        self.model = model
        model.elemdict[self.id] = self

    def calc_Rmatrix(self):
        import scipy
        import scipy.sparse as ss
        # a --> alpha, b --> beta, g --> gama
        cosb = alg3dpy.cosplanevec(alg3dpy.XY, self.xvec)
        sinb = alg3dpy.sinplanevec(alg3dpy.XY, self.xvec)
        cosg = alg3dpy.cosplanevec(alg3dpy.XZ, self.xvec)
        sing = alg3dpy.sinplanevec(alg3dpy.XZ, self.xvec)
        if self.__class__.__name__.find('ElemRod') == -1:
            Y2 = alg3dpy.Y * cosg - alg3dpy.X * sing
            cosa = alg3dpy.cos2vecs(Y2, self.yvec)
            sina = alg3dpy.sin2vecs(Y2, self.yvec)
        else:
            cosa = 1.
            sina = 0.
        gridnum = scipy.array(len(self.grids),dtype='int8')
        dim = gridnum * 6
        tmp = scipy.array(\
           [ cosb*cosg               ,  cosb*sing ,                  -sinb ,
            -cosa*sing+cosg*sina*sinb,  cosa*cosg+sina*sinb*sing, cosb*sina,
             sina*sing+cosa*cosg*sinb, -cosg*sina+cosa*sinb*sing, cosa*cosb],\
             dtype='float32')
        row = scipy.array([0, 0, 0, 1, 1, 1, 2, 2, 2], dtype='int8') 
        col = scipy.array([0, 1, 2, 0, 1, 2, 0, 1, 2], dtype='int8')
        self.Rcoord2el = ss.coo_matrix((tmp, (row, col)), shape = (3,3),\
                            dtype='float32')
        self.Rcoord2global = self.Rcoord2el.transpose()
        #
        data = scipy.array(scipy.zeros( 18*gridnum ))
        for i in xrange( gridnum ):
            for j in xrange(9):
                data[ 18*i + j ] = tmp[j] 
        row = scipy.array(\
            [i for i in xrange(dim) for j in xrange( 3 )], dtype='int8')
        col = scipy.array(\
            [j + int(i/3)*3 for i in xrange(dim) for j in xrange( 3 )],
            dtype='int8')
                
        #self.R2el converts from the global to the elements'
        self.R2el = ss.coo_matrix((data, (row, col)), shape = (dim,dim),
                                  dtype='float32')
        self.R2global = self.R2el.transpose()
        
    def build_k(self):
        import scipy
        import scipy.sparse as ss
        self.kelem = ss.coo_matrix( self.kelem )
        R = self.R2el.tocsc()
        Rinv = self.R2global.tocsc()
        kelem = self.kelem.tocsc()
        k = np.dot( Rinv, kelem )
        k = np.dot( k, R )
        self.k = k.tocoo()
       

    def calc_displ(self):
        self.displ = {}
        for sub in self.model.subcases.values():
            displ = scipy.zeros(0)
            for grid in self.grids:
                count = 0
                lst = [count*6 for i in xrange(6)]
                scipy.insert( displ, lst, grid.displ[sub.id] )
                count += 1
            self.displ[sub.id] = self.R2el * displ

