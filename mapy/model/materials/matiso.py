from mapy.model.materials import Materials
from mapy.reader import user_setattr
class MatIso(Materials):
    """
    Defines an isotropic material.
        
    Attributes:
    ____________________________________________________________________________
    card       the card name (NASTRAN etc)
    entryclass path to the class name
    id         material id
    e          Young Modulus
    g          shear modulus 
    nu         Poisson's ratio
    rho        especific mass (mass / volume)
    a          thermal expansion coeffiecient
    tref       reference temperature
    damp       structural damping coefficient
    st         allowable stress for tension
    sc         allowable stress for compression
    ss         allowable stress for shear
    mcsid      material coordinate system NOT USED
    ____________________________________________________________________________

    Note: when the user defines "nu" and "g", the "g" will be recaculated
          based on equation: e = 2*(1+nu)*g
    ____________________________________________________________________________
    """
    __slots__ = ['card','entryclass','id','e','g','nu','rho','a','tref',
                 'damp','st','sc','ss','mcsid']

    def __init__( self, id=None, e=None, nu=None ):
        super( MatIso, self ).__init__()
        self.id = id
        self.e = e
        self.nu = nu
        self.g = None
        self.rho = None
        self.a = None
        self.tref = None
        self.dampcoe = None
        self.st = None
        self.sc = None
        self.ss = None
        self.mcsid = None

    def read_inputs( self, inputs = {} ):
        if len( inputs ) > 0:
            self = user_setattr( self, inputs )
        
