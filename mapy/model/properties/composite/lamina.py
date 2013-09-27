import numpy as np
from mapy.constants import ONE, ZER, FLOAT
#
class Lamina(object):
    #TODO
    #    __slots__ = []
    """
    Reference: Reddy, J. N., Mechanics of Laminated Composite Plates and
    Shells - Theory and Analysys. Second Edition. CRC PRESS, 2004.


    Attributes:
    ____________________________________________________________________________

    plyid      id of the composite lamina
    matobj     a pointer to a MatLamina object
    t          ply thickness
    theta      ply angle
    thetarad   False means theta in degrees; True means theta in radians
    L          transformation matrix for displacements to laminate csys
    R          transformation matrix for stresses to laminate csys
    T          transformation matrix for stresses to lamina csys
    Q          constitutive matrix for plane-stress in lamina csys
    QL         constitutive matrix for plane-stress in laminate csys
    C          general constitutive matrix in lamina csys
    CL         general constitutive matrix in laminate csys
    laminates  laminates that contain this lamina
    cos        cos(   theta )
    cos2t      cos( 2*theta )
    sin        sin(   theta )
    sin2t      sin( 2*theta )
    ____________________________________________________________________________

    Note:
    ____________________________________________________________________________
    """
    def __init__(self):
        self.plyid    = None
        self.matobj   = None
        self.t        = None
        self.theta    = None
        self.thetarad = False
        self.L        = None
        self.R        = None
        self.T        = None
        self.Q        = None
        self.QL       = None
        self.laminates = []
        self.cos      = None
        self.cos2t    = None
        self.sin      = None
        self.sin2t    = None

    def rebuild( self ):
        if self.thetarad:
            self.thetarad = False
            self.theta = np.rad2deg( self.theta )
        self.cos   = np.cos( np.deg2rad(   self.theta ) )
        self.cos2t = np.cos( np.deg2rad( 2*self.theta ) )
        self.sin   = np.sin( np.deg2rad(   self.theta ) )
        self.sin2t = np.sin( np.deg2rad( 2*self.theta ) )
        #
        cos    = self.cos
        sin    = self.sin
        cos2   = cos**2
        cos3   = cos**3
        cos4   = cos**4
        sin2t  = self.sin2t
        sin2   = sin**2
        sin3   = sin**3
        sin4   = sin**4
        sincos = sin*cos
        self.L = np.array(\
            [[  cos,  sin, ZER ],
             [ -sin,  cos, ZER ],
             [  ZER,  ZER, ONE ]], dtype=FLOAT)
        #STRESS
        #to lamina
        self.R = np.array(\
            [[    cos2,    sin2, ZER,  ZER,  ZER,        sin2t ],
             [    sin2,    cos2, ZER,  ZER,  ZER,       -sin2t ],
             [     ZER,     ZER, ONE,  ZER,  ZER,          ZER ],
             [     ZER,     ZER, ZER,  cos, -sin,          ZER ],
             [     ZER,     ZER, ZER,  sin,  cos,          ZER ],
             [ -sincos,  sincos, ZER,  ZER,  ZER,    cos2-sin2 ]],dtype=FLOAT)
        #to laminate
        self.T = np.array(\
            [[    cos2,    sin2, ZER,  ZER,  ZER,       -sin2t ],
             [    sin2,    cos2, ZER,  ZER,  ZER,        sin2t ],
             [     ZER,     ZER, ONE,  ZER,  ZER,          ZER ],
             [     ZER,     ZER, ZER,  cos,  sin,          ZER ],
             [     ZER,     ZER, ZER, -sin,  cos,          ZER ],
             [  sincos, -sincos, ZER,  ZER,  ZER,    cos2-sin2 ]],dtype=FLOAT)
        #STRAINS
        #different from stress due to:
        #    2*e12 = e6    2*e13 = e5    2*e23 = e4
        #to laminate
        #self.Rstrain = np.transpose( self.Tstress )
        #to lamina
        #self.Tstrain = np.transpose( self.Rstress )
        if self.matobj.__class__.__name__ == "MatLamina":
            e1   = self.matobj.e1
            e2   = self.matobj.e2
            e3   = self.matobj.e3
            nu12 = self.matobj.nu12
            nu21 = self.matobj.nu21
            nu13 = self.matobj.nu13
            nu31 = self.matobj.nu31
            nu23 = self.matobj.nu23
            nu32 = self.matobj.nu32
            g12  = self.matobj.g12
            g13  = self.matobj.g13
            g23  = self.matobj.g23
        else:
            e1   = self.matobj.e
            e2   = self.matobj.e
            nu12 = self.matobj.nu
            nu21 = self.matobj.nu
            g12  = self.matobj.g
            g  = self.matobj.g
        # GENERAL CASE
        self.C  = self.matobj.c
        self.CL = np.dot( np.dot( self.T, self.C ), self.T.transpose() )
        # PLANE STRESS
        # from references:
        #   Reddy, J. N., Mechanics of laminated composite plates and shells.
        #   Theory and analysis. Second Edition. CRC Press, 2004.
        q11  = e1/(1-nu12*nu21)
        q12  = nu12*e2/(1-nu12*nu21)
        q22  = e2/(1-nu12*nu21)
        q44  = g23
        q55  = g13
        q16 = ZER
        q26 = ZER
        q66  = g12
        #
        self.Q = np.array(\
            [[ q11, q12, q16, ZER, ZER ],
             [ q12, q22, q26, ZER, ZER ],
             [ q16, q26, q66, ZER, ZER ],
             [ ZER, ZER, ZER, q44, ZER ],
             [ ZER, ZER, ZER, ZER, q55 ]], dtype=FLOAT )
        #
        q11L = q11*cos4 + 2*(q12 + 2*q66)*sin2*cos2 + q22*sin4
        q12L = (q11 + q22 - 4*q66)*sin2*cos2 + q12*(sin4 + cos4)
        q22L = q11*sin4 + 2*(q12 + 2*q66)*sin2*cos2 + q22*cos4
        q16L = (q11 - q12 - 2*q66)*sin*cos3 + (q12 - q22 + 2*q66)*sin3*cos
        q26L = (q11 - q12 - 2*q66)*sin3*cos + (q12 - q22 + 2*q66)*sin*cos3
        q66L = (q11 + q22 - 2*q12 - 2*q66)*sin2*cos2 + q66*(sin4 + cos4)
        q44L = q44*cos2 + q55*sin2
        q45L = (q55 - q44)*sincos
        q55L = q55*cos2 + q44*sin2
        #
        self.QL = np.array(\
            [[ q11L, q12L, q16L,  ZER,  ZER ],
             [ q12L, q22L, q26L,  ZER,  ZER ],
             [ q16L, q26L, q66L,  ZER,  ZER ],
             [  ZER,  ZER,  ZER, q44L, q45L ],
             [  ZER,  ZER,  ZER, q45L, q55L ]], dtype=FLOAT )
        self.TQ = np.array(\
            [[    cos2,    sin2,    -sin2t,  ZER,  ZER ],
             [    sin2,    cos2,     sin2t,  ZER,  ZER ],
             [  sincos, -sincos, cos2-sin2,  ZER,  ZER ],
             [     ZER,     ZER,       ZER,  cos,  sin ],
             [     ZER,     ZER,       ZER, -sin,  cos ]], dtype=FLOAT )
        self.RQ = np.array(\
            [[    cos2,    sin2,     sin2t,  ZER,  ZER ],
             [    sin2,    cos2,    -sin2t,  ZER,  ZER ],
             [ -sincos,  sincos, cos2-sin2,  ZER,  ZER ],
             [     ZER,     ZER,       ZER,  cos, -sin ],
             [     ZER,     ZER,       ZER,  sin,  cos ]], dtype=FLOAT )
        self.QL2 = np.dot( np.dot( self.TQ, self.Q ), self.TQ.transpose() )
        #
        #TODO add the thermal coeficient terms when calculating the
        #stresses... to discount eventual thermal expansions /
        #contractions

    def C2lamina( self, C ):
        return np.dot( np.dot( self.Tstress, C ), np.transpose(self.Tstress) )

    def S2lamina( self, S ):
        return np.dot( np.dot( np.transpose(self.Rstress), S ), self.Rstress )

class EqLamina( object ):
    """
    Attributes:
    ____________________________________________________________________________

    id         laminate property id
    laminates  list of laminates that can be part of this laminate
    plies      list of plies
    t          total thickness of the laminate
    eq_fracts  list of porcentages of each orientation
    eq_thetas  list of angles corresponding to eq_fracts
    eq_matobjs list of materials corresponding to eq_fracts

    ____________________________________________________________________________

    Note:
    ____________________________________________________________________________
    """
    def __init__(self):
        super( Laminate, self ).__init__()
        self.id   = None
        self.laminates = []
        self.plies     = []
        self.t    = None
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

    def eq_laminate( self ):
        #checks
        norm = False
        if sum(eq_fracts) <> 1.:
            self.print_warning([
                'angle fractions different then 1.',
                'automatically normalizing for calculations'])
            norm = True
        if norm:
            fracts = [float(i)/sum(eq_fracts) for i in eq_fracts]
        else:
            fracts = eq_fracts
        #
        if len(eq_fracts) <> len(eq_thetas):
            self.print_error([
                'number of angles differs from number of fractions'])
        #
        if len(eq_fracts) <> len(eq_matobjs):
            self.print_warning([
                'numer of matobj differs from number of fractions',
                'automatically assigning materials'])
            addnum = len( fractions ) - len(eq_matobjs)
            matobjref = eq_matobjs[0]
            matobjs = []
            for i in range( len(eq_fracts) ):
                matobjs.append( matobjref )
        else:
            matobjs = eq_matobjs
        #calculating eq_laminate
        self.e1  = 0.
        self.e2  = 0.
        self.e3  = 0.
        self.g23 = 0.
        self.g13 = 0.
        self.g12 = 0.
        for i in range( len(eq_thetas) ):
            fract  = fracts[i]
            theta  = thetas[i]
            matobj = matobjs[i]
            ply = Lamina()
            ply.matobj = matobj
            ply.theta = theta
            ply.calc_lamina()
            Rt = ply.R.transpose()
            lamina_eng = np.array(\
                [[ matobj.e1  ],
                 [ matobj.e2  ],
                 [ ONE        ],
                 [ matobj.g23 ],
                 [ matobj.g13 ],
                 [ matobj.g12 ]] , dtype = FLOAT)
            e1,e2,e3,g23,g13,g12 = np.dot( np.dot( Rt, ply.T ), lamina_eng )
            self.e1  += e1  * fract
            self.e2  += e2  * fract
            self.e3  += e3  * fract
            self.g23 += g23 * fract
            self.g13 += g13 * fract
            self.g12 += g12 * fract

