from mapy.reader import user_setattr
from alg3dpy import Point
from coords import Coord, CoordR, CoordC, CoordS
from mapy.constants import *
import numpy as np
import random as rdm

class Grid( Point ):
    """
    The inheritance from the alg3dpy.Point class exists.
    The array attribute is from Point class.

    Attributes:
    ____________________________________________________________________________
    card       the card name (NASTRAN etc)
    entryclass path to the class name
    id         grid id
    rcid       reference coordinate system id
    rcobj      pointer to the reference coordinate system object
    x1, x2, x3 coordinates
    ocid       output coordsys id
    ocobj      pointer to the ouptut coordsys
    perm_cons  permanent constraints, applied to all load cases
    seid       superelement id
    cons       dictionary that will be filled with all constraints applied
               to this grid
    loads      dictionary that will be filled with all loads applied to 
               this grid
    displ      dictionary that will store displacement resiults
    pos        defines the grid position in the stiffness matrix
               (for the solver)
    k_offset   used by the solver to store positions in the stiffness
               matrix, for each subcase
    elements   all elements connected to this grid
    garray     stores in a numpy array the original coordinates of this
               grid
    array      point-like coordinates, always given in the basic cartesian
               coordinate system, used to create other coordsys
    model      pointer to the model it belong to           
    rebuilt    pointer to the model it belong to           
    ____________________________________________________________________________

    """
    __slots__ = [ 'card','entryclass','id','rcid','rcobj','x1','x2','x3',\
                  'ocid','ocobj','perm_cons','seid','loads','cons','displ',\
                  'pos','k_offset', 'elements','garray','array','model' ]

    def __init__( self, inputs = {} ):
        self.card = None
        self.entryclass = None 
        self.id = int( MAXID*rdm.random() )
        self.rcid = None
        self.rcobj = None
        self.x1 = None
        self.x2 = None
        self.x3 = None
        self.ocid = None
        self.ocobj = None
        self.perm_cons = set()
        self.seid = None
        self.cons = {}
        self.loads = {}
        self.displ = {}
        self.pos = -1
        self.k_offset = {}
        self.elements = {}
        self.garray = None
        self.array = None
        self.model = None
        self.rebuilt = False
        self = self.read_inputs( inputs )

    def read_inputs( self, inputs = {} ):
        self = user_setattr(self, inputs)
        if self.perm_cons.__class__.__name__ <> 'set':
            str_perm_cons = self.perm_cons
            self.perm_cons = set([int(dof) for dof in str_perm_cons])
        #checking strings
        if self.rcid == '' \
        or self.rcid == None:
            self.rcid = 0
        if self.ocid == '' \
        or self.ocid == None:
            self.ocid = 0
        #updating he pointers to CSYSGLOBAL if rcid and ocid == 0
        if self.rcid == 0:
            self.rcobj = CSYSGLOBAL
        if self.ocid == 0:
            self.ocobj = CSYSGLOBAL
        self.garray = np.array([ self.x1, self.x2, self.x3 ], dtype=FLOAT)

    def check_to_rebuild( self ):
        self.rcobj = self.model.coorddict[ int(self.rcid) ]
        if self.rcobj.rebuilt:
            return True
        else:
            return False
        
    def rebuild( self ):
        self.cons = {}
        self.loads = {}
        self.displ = {}
        self.pos = -1
        self.k_offset = {}
        self.elements = {}
        #TODO transformation from degrees to radians
        #study in the future if it is better to do all
        #transformations at once in a dedicated module
        if self.rcobj.rebuilt:
            if self.rcobj.card == 'CORD1C' or self.rcobj.card == 'CORD2C':
                self.garray[1] = self.garray[1] * np.pi / 180.
            if self.rcobj.card == 'CORD1S' or self.rcobj.card == 'CORD2S':
                self.garray[1] = self.garray[1] * np.pi / 180.
                self.garray[2] = self.garray[2] * np.pi / 180.
            array = self.rcobj.transform( self.garray, CSYSGLOBAL ) 
            super( Grid, self ).__init__( array, self.id )
        else:
            print 'The grid cannot be rebuilt, the coordsys has not'
            print 'been updated...'
            raise
        self.rebuilt = True


    def transform( self, new_csys=None ):
        """
        This function checks for an existing reference coordinate system and it
        performs the transformation if necessary.
        See further description in mapy.model.coords.Coord().transform().
        """
        if self.rcobj == None:
            return self.array
        else:
            if self.rcobj.rebuilt:
                return self.rcobj.transform( self.array, new_csys )
            else:
                print 'The transformation can not be done.'
                print 'The grid rcobj (coordsys) was not rebuilt...'
                raise
                
    def add2model( self, model ):
        self.model = model
        model.griddict[self.id] = self

    def add_load( self, sub_id, dof, load ):
        if not int(sub_id) in self.loads.keys():
            self.loads[sub_id] = [ ZERO for i in xrange(6) ]
        self.loads[sub_id][dof - 1] += load
    
    def add_cons( self, sub_id, dof ):
        if not int(sub_id) in self.cons.keys():
            self.cons[sub_id] = set([])
        if not dof in self.cons[sub_id]:
            self.cons[sub_id].add(dof)
        else:
            print 'Duplicated CONSTRAINT for GRID %d, dof %d' % (self.id, dof)
    
    def attach_displ( self, sub_id, displ_vec ):
        self.displ[sub_id] = displ_vec
    
    def read_card():
        #TODO if it is better to keep the card reading here instead of inside
        #     mapy.reader
        pass
    def print_card():
        #TODO if it is better to keep the card printing here instead of inside
        #     mapy.reader or mapy.printer
        pass

    def print_displ( self, sub_id ):
        if sub_id in self.displ.keys():
            d = self.displ[sub_id]
            print 'GRID,%d,SUB,%d,DISPL,%f,%f,%f,%f,%f,%f' %\
                  tuple([ self.id , sub_id ] + [t for t in d])

    def __str__( self ):
        return 'Grid ID %d:\n\
                \tCoord Sys ID %d:\n\
                \tx1 = %2.3f, x2 = %2.3f, x3 = %2.3f'\
                % (self.id, self.rcid, self.array[0], self.array[1], self.array[2])

    def __repr__( self ):
        return 'mapy.model.Grid class'


