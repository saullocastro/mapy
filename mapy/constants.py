from alg3dpy.vector import asvector
from alg3dpy.constants import Z, O, FLOAT, ZER, INT
from mapy.model.coords import CoordR
vecxz = asvector([1.,0.,1.])
CSYSGLOBAL = CoordR(0, O, None, Z, vecxz)
CSYSGLOBAL.rebuild(rcobj=None, force_new_axis=False)
CSYSGLOBAL.rcobj = CSYSGLOBAL
MAXID = 99999999

