import numpy as np
from lamina import Lamina
from mapy.model.properties import Properties
from mapy.model.materials.matlamina import read_laminaprop
from mapy.constants import ONE, ZER, FLOAT
class Laminate(Properties):

    #TODO update this __slots__
    #__slots__ = []

    """
    Attributes:
    ____________________________________________________________________________

    id         laminate property id
    general    laminate as general uses the general constitutive equations
    laminates  list of laminates that can be part of this laminate
    plies      list of plies
    plyts      ply thicknesses for this laminate
    t          total thickness of the laminate
    e1         equivalent laminate modulus in 1 direction
    e2         equivalent laminate modulus in 2 direction
    g12        equivalent laminate shear modulus in 12 direction
    nu12       equivalent laminate Poisson ratio in 12 direction
    nu21       equivalent laminate Poisson ratio in 21 direction
    eq_fracts  list of porcentages of each orientation
    eq_thetas  list of angles corresponding to eq_fracts
    eq_matobjs list of materials corresponding to eq_fracts
    xiA        laminate parameters for extensional matrix A
    xiB        laminate parameters for extension-bending matrix B
    xiD        laminate parameters for bending matrix D
    A          laminate extension matrix
    B          laminate extension-bending matrix
    D          laminate bending matrix
    E          laminate transferse shear matrix
    ABD        laminate ABD matrix
    ABDE       laminate ABD matrix with transverse shear terms
    ____________________________________________________________________________

    Note:
    ____________________________________________________________________________
    """
    def __init__(self):
        super(Laminate, self).__init__()
        self.id   = None
        self.general = False
        self.laminates = []
        self.plies   = []
        self.matobj = None
        self.t    = None
        self.plyts= []
        eq_thetas = None
        eq_fracts = None
        eq_matobjs = None
        self.e1   = None
        self.e2   = None
        self.e3   = None
        self.nu12 = None
        self.g12  = None
        self.g13  = None
        self.g23  = None
        self.xiA  = None
        self.xiB  = None
        self.xiD  = None
        self.A    = None
        self.B    = None
        self.D    = None
        self.E    = None
        self.ABD  = None
        self.ABDE = None

    def rebuild(self):
        T = ZER
        for ply in self.plies:
            ply.rebuild()
            T += ply.t
        self.t = T

    def calc_equivalent_modulus(self):
        AI = np.matrix(self.ABD, dtype=FLOAT).I
        a11, a12, a22, a33 = AI[0,0], AI[0,1], AI[1,1], AI[2,2]
        self.e1  = 1./(self.t*a11)
        self.e2  = 1./(self.t*a22)
        self.g12 = 1./(self.t*a33)
        self.nu12 = - a12 / a11
        self.nu21 = - a12 / a22

    def calc_lamination_parameters(self):
        #
        xiA1, xiA2, xiA3, xiA4 = ZER, ZER, ZER, ZER
        #
        xiB1, xiB2, xiB3, xiB4 = ZER, ZER, ZER, ZER
        #
        xiD1, xiD2, xiD3, xiD4 = ZER, ZER, ZER, ZER
        #
        xiE1, xiE2, xiE3, xiE4 = ZER, ZER, ZER, ZER
        #
        T = ZER
        #
        for ply in self.plies:
            T += ply.t
        self.t = T
        h0   = -T/2
        for ply in self.plies:
            #
            hk_1 =  h0
            h0   += ply.t
            hk   =  h0
            #
            Afac  = ply.t / T
            Bfac  = (2. / T**2) * (hk**2 - hk_1**2)
            Dfac  = (4. / T**3) * (hk**3 - hk_1**3)
            Efac  = (1. / T   ) * (hk    - hk_1   )# * (5./6) * (5./6)
            #
            cos2t = ply.cos2t
            cos4t = ply.cos4t
            sin2t = ply.sin2t
            sin4t = ply.sin4t
            #
            xiA1  += Afac * cos2t
            xiA2  += Afac * sin2t
            xiA3  += Afac * cos4t
            xiA4  += Afac * sin4t
            #
            xiB1  += Bfac * cos2t
            xiB2  += Bfac * sin2t
            xiB3  += Bfac * cos4t
            xiB4  += Bfac * sin4t
            #
            xiD1  += Dfac * cos2t
            xiD2  += Dfac * sin2t
            xiD3  += Dfac * cos4t
            xiD4  += Dfac * sin4t
            #
            xiE1  += Efac * cos2t
            xiE2  += Efac * sin2t
            xiE3  += Efac * cos4t
            xiE4  += Efac * sin4t
        #
        self.xiA = np.array([ ONE, xiA1, xiA2, xiA3, xiA4], dtype=FLOAT)
        self.xiB = np.array([ ZER, xiB1, xiB2, xiB3, xiB4], dtype=FLOAT)
        self.xiD = np.array([ ONE, xiD1, xiD2, xiD3, xiD4], dtype=FLOAT)
        self.xiE = np.array([ ONE, xiE1, xiE2, xiE3, xiE4], dtype=FLOAT)

    def calc_ABDE_from_lamination_parameters(self):
        # dummies used to unpack vector results
        du1, du2, du3, du4, du5, du6 = ZER, ZER, ZER, ZER, ZER, ZER
        # A matrix terms
        A11,A22,A12, du1,du2,du3, A66,A16,A26 =\
            (self.t       ) * np.dot(self.matobj.u, self.xiA)
        # B matrix terms
        B11,B22,B12, du1,du2,du3, B66,B16,B26 =\
            (self.t**2/4. ) * np.dot(self.matobj.u, self.xiB)
        # D matrix terms
        D11,D22,D12, du1,du2,du3, D66,D16,D26 =\
            (self.t**3/12.) * np.dot(self.matobj.u, self.xiD)
        # E matrix terms
        du1,du2,du3, E44,E55,E45, du4,du5,du6 =\
            (self.t       ) * np.dot(self.matobj.u, self.xiE)
        #
        self.A = np.array([[ A11, A12, A16 ],
                           [ A12, A22, A26 ],
                           [ A16, A26, A66 ]], dtype=FLOAT)
        #
        self.B = np.array([[ B11, B12, B16 ],
                           [ B12, B22, B26 ],
                           [ B16, B26, B66 ]], dtype=FLOAT)
        #
        self.D = np.array([[ D11, D12, D16 ],
                           [ D12, D22, D26 ],
                           [ D16, D26, D66 ]], dtype=FLOAT)
        #
        # printing E acoordingly to Reddy definition for E44, E45 and E55
        self.E = np.array([[ E55, E45 ],
                            [ E45, E44 ]], dtype=FLOAT)
        #
        self.ABD  = np.array([[ A11, A12, A16, B11, B12, B16 ],
                              [ A12, A22, A26, B12, B22, B26 ],
                              [ A16, A26, A66, B16, B26, B66 ],
                              [ B11, B12, B16, D11, D12, D16 ],
                              [ B12, B22, B26, D12, D22, D26 ],
                              [ B16, B26, B66, D16, D26, D66 ]], dtype=FLOAT)
        #
        # printing ABDE acoordingly to Reddy definition for E44, E45 and E55
        self.ABDE = np.array([[ A11, A12, A16, B11, B12, B16, ZER, ZER ],
                              [ A12, A22, A26, B12, B22, B26, ZER, ZER ],
                              [ A16, A26, A66, B16, B26, B66, ZER, ZER ],
                              [ B11, B12, B16, D11, D12, D16, ZER, ZER ],
                              [ B12, B22, B26, D12, D22, D26, ZER, ZER ],
                              [ B16, B26, B66, D16, D26, D66, ZER, ZER ],
                              [ ZER, ZER, ZER, ZER, ZER, ZER, E55, E45 ],
                              [ ZER, ZER, ZER, ZER, ZER, ZER, E45, E44 ]],
                               dtype=FLOAT)

    def calc_ABD_general(self):
        self.A_general = np.zeros([5,5], dtype=FLOAT)
        self.A         = np.zeros([3,3], dtype=FLOAT)
        self.B_general = np.zeros([5,5], dtype=FLOAT)
        self.B         = np.zeros([3,3], dtype=FLOAT)
        self.D_general = np.zeros([5,5], dtype=FLOAT)
        self.D         = np.zeros([3,3], dtype=FLOAT)
        self.E         = np.zeros([2,2], dtype=FLOAT)
        T = ZER
        #
        for ply in self.plies:
            T += ply.t
        self.t = T
        h0   = -T/2
        for ply in self.plies:
            #
            hk_1 =  h0
            h0   += ply.t
            hk   =  h0
            for i in range(5):
                for j in range(5):
                    self.A_general[i][j] +=     ply.QL[i][j]*(hk    - hk_1  )
                    self.B_general[i][j] +=1/2.*ply.QL[i][j]*(hk**2 - hk_1**2)
                    self.D_general[i][j] +=1/3.*ply.QL[i][j]*(hk**3 - hk_1**3)
            self.A = self.A_general[0:3,0:3]
            self.B = self.B_general[0:3,0:3]
            self.D = self.D_general[0:3,0:3]
            for iE, iQ in enumerate([3,4]):
                for jE, jQ in enumerate([3,4]):
                    self.E[iE][jE] += ply.QL[iQ][jQ] * (hk    - hk_1  )
        conc1 = np.concatenate([ self.A_general, self.B_general ], axis=1)
        conc2 = np.concatenate([ self.B_general, self.D_general ], axis=1)
        self.ABD_general = np.concatenate([conc1, conc2], axis=0)
        conc1 = np.concatenate([ self.A, self.B ], axis=1)
        conc2 = np.concatenate([ self.B, self.D ], axis=1)
        self.ABD = np.concatenate([conc1, conc2], axis=0)
        self.ABDE = np.zeros((8,8), dtype=FLOAT)
        self.ABDE[:6,:6] = self.ABD
        self.ABDE[6:8,6:8] = self.E

    def force_balanced_LP(self):
        ONE, xiA1, xiA2, xiA3, xiA4 = self.xiA
        self.xiA = np.array([ ONE, xiA1, ZER, xiA3, ZER], dtype=FLOAT)
        self.calc_ABDE_from_lamination_parameters()

    def force_symmetric_LP(self):
        self.xiB = np.zeros(5)
        self.calc_ABDE_from_lamination_parameters()

    def force_balanced(self):
        self.A[0][2] = ZER
        self.A[1][2] = ZER
        self.A[2][0] = ZER
        self.A[2][1] = ZER
        self.ABD[0][2] = ZER
        self.ABD[1][2] = ZER
        self.ABD[2][0] = ZER
        self.ABD[2][1] = ZER
        self.ABDE[0][2] = ZER
        self.ABDE[1][2] = ZER
        self.ABDE[2][0] = ZER
        self.ABDE[2][1] = ZER

    def force_symmetric(self):
        self.B = np.zeros((3,3))
        for i in range(0,3):
            for j in range(3,6):
                self.ABD[i][j]  = ZER
                self.ABDE[i][j] = ZER
        for i in range(3,6):
            for j in range(0,3):
                self.ABD[i][j]  = ZER
                self.ABDE[i][j] = ZER

    def read_stack(self, stack, plyts, laminaprop=None, laminaprops=[]):
        if isinstance(plyts, list):
            self.plyts = plyts
        else:
            self.plyts = [plyts for i in stack]
        self.stack = stack
        if not laminaprops:
            if not laminaprop:
                print 'mapy - laminate - read_stack() - must input laminaprop'
                print 'or laminaprops'
                return None
            laminaprops = [laminaprop for i in stack]
        for i, theta in enumerate(self.stack):
            laminaprop = laminaprops[i]
            self.matobj = read_laminaprop(laminaprop)
            ply = Lamina()
            ply.theta = np.array(theta, dtype=FLOAT)
            ply.t = np.array(self.plyts[i], dtype=FLOAT)
            ply.matobj = self.matobj
            self.plies.append(ply)
        self.rebuild()
        if self.general == False:
            self.calc_lamination_parameters()
            self.calc_ABDE_from_lamination_parameters()
        else:
            self.calc_ABD_general()
        return self


    def read_lamination_parameters(xiA1, xiA2, xiA3, xiA4,
                                    xiB1, xiB2, xiB3, xiB4,
                                    xiD1, xiD2, xiD3, xiD4,
                                    xiE1, xiE2, xiE3, xiE4, laminaprop = None):
        lam.matobj = read_laminaprop(laminaprop)
        self.xiA = np.array([ ONE, xiA1, xiA2, xiA3, xiA4 ], dtype=FLOAT)
        self.xiB = np.array([ ZER, xiB1, xiB2, xiB3, xiB4 ], dtype=FLOAT)
        self.xiD = np.array([ ONE, xiD1, xiD2, xiD3, xiD4 ], dtype=FLOAT)
        self.xiE = np.array([ ONE, xiE1, xiE2, xiE3, xiE4 ], dtype=FLOAT)

def read_stack(stack, plyts, laminaprop=None, laminaprops=[], general = True):
    '''
    laminaprop = (E11, E22, nu12, G12, G13, G23, tempref, E33, nu13, nu23)
    '''
    lam = Laminate()
    lam.general = general
    lam.read_stack(stack, plyts, laminaprop, laminaprops)
    return lam

def read_lamination_parameters(xiA1, xiA2, xiA3, xiA4,
                                xiB1, xiB2, xiB3, xiB4,
                                xiD1, xiD2, xiD3, xiD4,
                                xiE1, xiE2, xiE3, xiE4, laminaprop = None):
    lam = Laminate()
    lam.general = False
    lam.read_lamination_parameters(xiA1, xiA2, xiA3, xiA4,
                                    xiB1, xiB2, xiB3, xiB4,
                                    xiD1, xiD2, xiD3, xiD4,
                                    xiE1, xiE2, xiE3, xiE4, laminaprop)
    return lam

