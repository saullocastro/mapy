from alg3dpy.vector import Vec
from alg3dpy.angles import cosplanevec, sinplanevec, cos2vecs, sin2vecs
from alg3dpy.plane import Plane
from alg3dpy.point import Point
import random as rdm
import numpy as np
import mapy
from mapy.reader import user_setattr
from mapy.constants import *

def common__str__(text, csys):
    if csys.rebuilt:
        return '%s ID %d:\n\
        \tO %2.3f i + %2.3f j + %2.3f k\n\
        \tX %2.3f i + %2.3f j + %2.3f k\n\
        \tY %2.3f i + %2.3f j + %2.3f k\n\
        \tZ %2.3f i + %2.3f j + %2.3f k' \
        % ( text, csys.id,\
            csys.o[0], csys.o[1], csys.o[2],\
            csys.x[0], csys.x[1], csys.x[2],\
            csys.y[0], csys.y[1], csys.y[2],\
            csys.z[0], csys.z[1], csys.z[2] )
    else:
        return '%s ID %d:\n\
        \tNOT REBUILT...'\
        % ( text, csys.id )
        

class Coord(object):
    """
    Each coordinate system is defined by three points:
        rcid: reference coordinate system in which all the others are
             defined. If not given the basic cartesian system will be used.
        o:  the origin
        z:  the Z axis
        vecxz: a point laying in the azimuthal origin
    Basically the point are defined using reference GRIDs or POINT coordinates.
        
    Attributes:
    ____________________________________________________________________________
    card       the card name (NASTRAN etc)
    entryclass path to the class name
    id         coordinate system id
    rcid       reference coordsys id
    rcobj      pointer to the reference coordsys object
    o          the origin of the coordsys alg3dpy.Point
    x          the x vector of the coordsys
    y          the y vector of the coordsys
    z          the z vector of the coordsys
    xy         the xy plane of the coordsys
    xz         the xz plane of the coordsys
    yz         the yz plane of the coordsys
    vecxz      a vector laying in the xz plane of the coordsys
    a1, a2, a3 components of the point defining the origin
    b1, b2, b3 components of the point defining the y axis
    c1, c2, c3 components of the point defining the xz plane
    ida, idb   id of coordsys "a" or "b" when creating two coordsys in the
               same card. In NASTRAN, the cards: CORD1R, CORD1C or CORD1S
    g1a, g1b   grid defining the origin of coordsys "a" or "b" 
    g2a, g2b   grid defining the z axis of coordsys "a" or "b" 
    g3a, g3b   grid defining the xz plane of coordsys "a" or "b" 
    model      pointer to the model object it belongs to
    rebuilt    a flag to tell if this coordsys is already rebuilt
    ____________________________________________________________________________

    Note: not all attributes are used simultaneously, but the Coord class is
          already prepared for many ways for defining a coordsys
    ____________________________________________________________________________
    """
    __slots__ = [ 'card','entryclass','id','rcid','rcobj','o','x','y','z',
                  'xy','xz','yz','vecxz',
                  'a1','a2','a3','b1','b2','b3','c1','c2','c3',
                  'ida','idb','g1a','g2a','g3a','g1b','g2b','g3b',
                  'model','rebuilt' ]

    def __init__(self, id=None, o=None, rcid=None, z=None, vecxz=None):
        self.card = None
        self.entryclass = None
        inputs = {}
        if id.__class__.__name__ == 'dict':
            inputs = id
            id = None
        self.id    = id 
        self.rcid  = rcid
        self.rcobj = None
        self.o     = o
        self.x     = None
        self.y     = None
        self.z     = z
        self.xy    = None
        self.xz    = None
        self.yz    = None
        self.vecxz = vecxz 
        self.a1    = None
        self.a2    = None
        self.a3    = None
        self.b1    = None
        self.b2    = None
        self.b3    = None
        self.c1    = None
        self.c2    = None
        self.c3    = None
        self.ida   = None
        self.idb   = None
        self.g1a   = None
        self.g2a   = None
        self.g3a   = None
        self.g1b   = None
        self.g2b   = None
        self.g3b   = None
        self.model = None
        self.rebuilt = False
        self.read_inputs( inputs )
        
    def read_inputs( self, inputs = {} ):
        if len(inputs) > 0:
            self = user_setattr(self, inputs)
        if self.id == None and self.ida <> None:
            self.id = int(self.ida)
            CSYSGLOBAL = mapy.constants.CSYSGLOBAL
            self.rcid = 0
            self.rcobj = CSYSGLOBAL
        
    def add2model(self, model):
        self.model = model
        model.coorddict[self.id] = self
        if  self.idb <> None\
        and self.g1b <> None and self.g2b <> None and self.g3b <> None:
            if self.__class__.__name__.find('CoordR') > -1:
                newcsys = CoordR( int(self.idb), None, None, None, None )
            if self.__class__.__name__.find('CoordC') > -1:
                newcsys = CoordC( int(self.idb), None, None, None, None )
            if self.__class__.__name__.find('CoordS') > -1:
                newcsys = CoordS( int(self.idb), None, None, None, None )
            newcsys.ida   = self.idb
            newcsys.id    = self.idb
            newcsys.rcid  = self.rcid
            newcsys.rcobj = self.rcobj
            newcsys.card  = self.card
            newcsys.entryclass = self.entryclass
            newcsys.g1a   = self.g1b
            newcsys.g2a   = self.g2b
            newcsys.g3a   = self.g3b
            newcsys.model = model
            model.coorddict[newcsys.id] = newcsys
            self.idb      = None
            self.g1b      = None
            self.g2b      = None
            self.g3b      = None

    def check_to_rebuild( self ):
        if   self.a1 <> None and self.a2 <> None and self.a3 <> None \
        and  self.b1 <> None and self.b2 <> None and self.b3 <> None \
        and  self.c1 <> None and self.c2 <> None and self.c3 <> None:
            rcobj = self.model.coorddict[ int(self.rcid) ]
            if rcobj.rebuilt:
                return True
            else:
                return False
        elif self.ida <> None \
        and  self.g1a <> None and self.g2a <> None and self.g3a <> None:
            g1a       = self.model.griddict[ int(self.g1a) ]
            g2a       = self.model.griddict[ int(self.g2a) ]
            g3a       = self.model.griddict[ int(self.g3a) ]
            if not g1a.rebuilt \
            or not g2a.rebuilt \
            or not g3a.rebuilt:
                return False
            else: 
                return True

        else:
            print 'FIXME'
            raise

    def rebuild(self, rcobj = None, force_new_axis = False ):
        new_axis = False
        if self.o == None or self.z == None or self.vecxz == None:
            new_axis = True
        if not new_axis:
            if self.o.__class__.__name__.find('Point') == -1:
                self.o = Point( np.array([ 0,0,0 ], dtype=FLOAT ) )
            if self.z == None:
                print 'Please, enter a valid z axis...'
                raise
            if self.vecxz == None:
                print 'Please, enter a valid vector in the xz plane...'
                raise
            if self.z.__class__.__name__.find('Vec') == -1:
                self.z = Vec( self.z )
            if self.vecxz.__class__.__name__.find('Vec') == -1:
                self.vecxz = Vec( self.vecxz )
        if new_axis or force_new_axis:
            if self.model == None:
                print 'The coordinate system must belong to a model...'
                print 'the user may create a coordsys giving directly:'
                print '- origin as a alg3dpy.Point'
                print '- z axis as a alg3dpy.Vec'
                print '- alg3dpy.Vec laying on xz plane'
                raise
            if   self.a1 <> None and self.a2 <> None and self.a3 <> None \
            and  self.b1 <> None and self.b2 <> None and self.b3 <> None \
            and  self.c1 <> None and self.c2 <> None and self.c3 <> None:
                self.rcobj = self.model.coorddict[ int(self.rcid) ]
                if self.rcobj.rebuilt:
                    #FIXME destroying the reference to rcobj original
                    p1 = np.array([self.a1, self.a2, self.a3], dtype=FLOAT)
                    p2 = np.array([self.b1, self.b2, self.b3], dtype=FLOAT)
                    p3 = np.array([self.c1, self.c2, self.c3], dtype=FLOAT)
                    CSYSGLOBAL = mapy.constants.CSYSGLOBAL
                    p1 = self.rcobj.transform( p1, CSYSGLOBAL )
                    p2 = self.rcobj.transform( p2, CSYSGLOBAL )
                    p3 = self.rcobj.transform( p3, CSYSGLOBAL )
                    self.rcid  = CSYSGLOBAL.id 
                    self.rcobj  = CSYSGLOBAL
                    self.o     = p1
                    self.z     = p2 - p1
                    self.vecxz = p3 - p1

                else:
                    print 'The coordsys cannot be rebuilt. The reference'
                    print 'coordsys given by rcid is not rebuilt...'
                    raise
            elif self.ida <> None\
            and  self.g1a <> None and self.g2a <> None and self.g3a <> None:
                g1a       = self.model.griddict[ int(self.g1a) ]
                g2a       = self.model.griddict[ int(self.g2a) ]
                g3a       = self.model.griddict[ int(self.g3a) ]
                if not g1a.rebuilt \
                or not g2a.rebuilt \
                or not g3a.rebuilt:
                    print 'The coordsys cannot be rebuilt. The reference'
                    print 'grids g1a, g2a and g3a are not rebuilt...'
                    raise
                self.o     = Point( g1a.array )
                self.z     = g2a - g1a
                self.vecxz = g3a - g1a 
            else:
                print 'Something wrong with your inputs'
                print 'Please, see all the attributes below:'
                for slot in self.__slots__:
                    print '\t' + slot + '', getattr(self, slot)
                raise 

        self.y  = self.z.cross( self.vecxz )
        self.x  = self.y.cross(     self.z )
        self.xy = Plane(  self.z[0],  self.z[1],  self.z[2], self.o.mod() ) 
        self.xz = Plane( -self.y[0], -self.y[1], -self.y[2], self.o.mod() )
        self.yz = Plane(  self.x[0],  self.x[1],  self.x[2], self.o.mod() )
        self.rebuilt = True
            
    def transform(self, vec, new_csys):
        """
        The transformation will go as follows:
            - transform to cartesian in the local coordsys;
            - rotate to the new_csys (which is cartesian);
            - translate to the new_csys.
        All systems: cartesian, cylindrical or spherical; have
        the method vec2cr which will automatically transform vec into
        cartesian coordinates in the local coordsys.
        The two other steps will rotate and translate vec to new_csys.
        The last step will transform again from the new_csys cartesian
        coordinates to its cylindrical or spherical coordinates.
        All coordinate systems have the method cr2me to transform from
        local cartesian to local something.
            
        """
        #FIXME modify this to keep the original reference to rcobj
        if new_csys == None:
            new_csys = CSYSGLOBAL 
        vec_cr = self.vec2cr( vec )
        R      = self.Rmatrix( new_csys )
        vec_rot = np.dot( R, vec_cr ) 
        vec_t  = self.translate( vec_rot, new_csys ) 
        vec_final = new_csys.cr2me( vec_t )
        return vec_final
                 
    def translate(self, vec, newcr):
        """
        Calculates the translation matrix to a new cartesian system (newcr)
        """
        vec = Vec( vec )
        vec_t = vec + newcr.o + self.o
        return vec_t

    def Rmatrix(self, newcr):
        """
        Calculates the rotation matrix to a new cartesian system (newcr)
        """
        cosb = cosplanevec( newcr.xy, self.x )
        sinb = sinplanevec( newcr.xy, self.x )
        cosg = cosplanevec( newcr.xz, self.x )
        sing = sinplanevec( newcr.xz, self.x )
        tmpT =  np.array([\
            [ -sing,  ZER, ZER ],
            [   ZER, cosg, ZER ],
            [   ZER,  ZER, ZER ]])
        Y2 = Vec( np.dot( tmpT, newcr.y.array ) )
        cosa = cos2vecs( Y2, self.y )
        sina = sin2vecs( Y2, self.y )
        Rself = np.array([\
           [ cosb*cosg               ,  cosb*sing ,                  -sinb ], \
           [-cosa*sing+cosg*sina*sinb,  cosa*cosg+sina*sinb*sing, cosb*sina], \
           [ sina*sing+cosa*cosg*sinb, -cosg*sina+cosa*sinb*sing, cosa*cosb]],\
                                                                  dtype=FLOAT)
        R2new = Rself.transpose()
        return R2new

    def R2basic(self):
        return self.Rmatrix( CSYSGLOBAL )

class CoordR(Coord):
    def __init__(self, id=None, o=None, rcid=None, z=None, vecxz=None):
        super( CoordR, self ).__init__(id, o, rcid, z, vecxz)

    def __str__(self):
        return common__str__('Cartesian Coord Sys', self)

    def vec2cr( self, vec ):
        return vec

    def cr2me( self, vec ):
        return vec

class CoordC(Coord):
    def __init__(self, id=None, o=None, rcid=None, z=None, vecxz=None):
        super( CoordC, self ).__init__(id, o, rcid, z, vecxz)

    def vec2cr( self, vec ):
        """
        Transformation from cylindrical to cartesian
        vec must be in cylindrical cordinates: [r, theta, z]
        """
        T =  np.array([\
            [ np.cos( vec[1] ), ZER,   ZER ],
            [ ZER, np.sin( vec[1] ),   ZER ],
            [ ZER,                ZER, ONE ]])
        tmp = np.array([ vec[0], vec[0], vec[2] ], dtype=FLOAT) 
        vec_cr = np.dot( T, tmp ) 
        return vec_cr
    
    def cr2me( self, vec ):
        """
        Transformation from cartesian to cylindrical
        vec must be in cartesian coordinates: [x, y, z]
        """
        T = np.array([\
            [ np.sqrt( vec[0] ** 2 + vec[1] ** 2 ), ZER,   ZER ],
            [ ZER,           np.arctan( vec[1] / vec[0] ),   ZER ],
            [ ZER,                                    ZER, ONE ]])
        tmp = np.array([ 1, 1, vec[2] ], dtype=FLOAT) 
        return np.dot( T, tmp )

    def __str__(self):
        return common__str__('Cylindrical Coord Sys', self)

class CoordS(Coord):
    def __init__(self, id=None, o=None, rcid=None, z=None, vecxz=None):
        super( CoordS, self ).__init__(id, o, rcid, z, vecxz)

    def vec2cr( self, vec ):
        """
        Transformation from spherical to cartesian
        vec must be in spherical coordinates: [r, theta, phi]
        """
        T =  np.array([\
            [ np.sin( vec[1] )*np.cos( vec[2] ), ZER, ZER ],
            [ ZER, np.sin( vec[1] )*np.sin( vec[2] ), ZER ],
            [ ZER, ZER,                  np.cos( vec[1] ) ]])
        tmp = np.array([ vec[0], vec[0], vec[0] ], dtype=FLOAT) 
        return np.dot( T, tmp )

    def cr2me( self, vec ):
        """
        Transformation from cartesian to spherical
        vec must be in cartesian coordinates: [x, y, z]
        """
        h = vec[0] ** 2 + vec[1] ** 2
        T = np.array([\
            [ np.sqrt( h + vec[2] ** 2 ),     ZER,   ZER ],
            [ ZER, np.arctan( np.sqrt(h) / vec[2] ),   ZER ],
            [ ZER,       ZER, np.arctan( vec[1] / vec[0] ) ]]) 
        tmp = np.array([ 1, 1, 1], dtype=FLOAT)
        return np.dot( T, tmp )

    def __str__(self):
        return common__str__('Spherical Coord Sys', self)

# Weisstein, Eric W. "Rotation Matrix." From MathWorld--A Wolfram Web Resource.
#   http://mathworld.wolfram.com/RotationMatrix.html 
