import numpy as np
from alg3dpy.constants import *
from mapy.model.coords import CoordR
vecxz = Vec( np.array((1,0,1), dtype=FLOAT) )
CSYSGLOBAL = CoordR(0, O, None, Z, vecxz )
CSYSGLOBAL.rebuild( rcobj = None, force_new_axis = False )
CSYSGLOBAL.rcobj = CSYSGLOBAL

