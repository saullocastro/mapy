import sympy
from sympy.core.power import Pow
import sys
from sympy.matrices import Matrix
sympy.var('x y x1 y1 x2 y2 x3 y3 z z1 z2 z3 area')
def area_tria(x1,x2,x3,y1,y2,y3,z1,z2,z3):
    a = sympy.sqrt(Pow(x2-x1,2) + Pow(y2-y1,2) + Pow(z2-z1,2))
    b = sympy.sqrt(Pow(x3-x1,2) + Pow(y3-y1,2) + Pow(z3-z1,2))
    c = sympy.sqrt(Pow(x3-x2,2) + Pow(y3-y2,2) + Pow(z3-z2,2))
    p = (a + b + c)/2.
    return sympy.sqrt( p*(p-a)*(p-b)*(p-c) )

L2 = area_tria(x,x1,x3,y,y1,y3,z,z1,z3)

L3 = area_tria(x,x2,x3,y,y2,y3,z,z2,z3) / area

print 'L2 =',L2
print 'L3 =',L3

sympy.pprint(L2)

print sys.argv





