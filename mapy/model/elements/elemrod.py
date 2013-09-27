from mapy.model.elements.elem1d import Elem1D
from mapy.reader import user_setattr
from mapy.constants import FLOAT, INT

class ElemRod(Elem1D):
    '''Defines a rod element, which is a truss including the axial
    torsion.
    '''
    def __init__(self, inputs):
        Elem1D.__init__(self)
        self = user_setattr(self, inputs)

    def rebuild(self):
        Elem1D.rebuild(self)
        self.A = self.pobj.a
        self.E = self.pobj.matobj.e
        self.calc_Rmatrix()
        self.build_kelem()

    def build_kelem(self):
        import scipy
        import scipy.sparse as ss
        #FIXME add J and the respective stiffness matrix terms
        A = self.A
        E = self.E
        L = self.L
        eal = E*A/L
        data = scipy.array([ eal,-eal,-eal, eal], dtype=FLOAT )
        row =  scipy.array([   0,   6,   0,   6], dtype=INT )
        col =  scipy.array([   0,   0,   6,   6], dtype=INT )
        self.kelem = ss.coo_matrix( (data,  (row, col)), shape=(12,12))
    
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
