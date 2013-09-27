import sympy
sympy.var('u v csi eta u1 u2 u3 u4 u5 u6 v1 v2 v3 v4 v5 v6')
sympy.var('c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12')
sympy.var('x1 x2 x3 x4 x5 x6 y1 y2 y3 y4 y5 y6')
#finding 'ci's
eq1  = - u1 + c1 + c2* x1 + c3* y1 +  c4* x1*y1 +  c5* x1*x1 +  c6* y1*y1
eq2  = - u2 + c1 + c2* x2 + c3* y2 +  c4* x2*y2 +  c5* x2*x2 +  c6* y2*y2
eq3  = - u3 + c1 + c2* x3 + c3* y3 +  c4* x3*y3 +  c5* x3*x3 +  c6* y3*y3
eq4  = - u4 + c1 + c2* x4 + c3* y4 +  c4* x4*y4 +  c5* x4*x4 +  c6* y4*y4
eq5  = - u5 + c1 + c2* x5 + c3* y5 +  c4* x5*y5 +  c5* x5*x5 +  c6* y5*y5
eq6  = - u6 + c1 + c2* x6 + c3* y6 +  c4* x6*y6 +  c5* x6*x6 +  c6* y6*y6
eq7  = - v1 + c7 + c8* x1 + c9* y1 + c10* x1*y1 + c11* x1*x1 + c12* y1*y1
eq8  = - v2 + c7 + c8* x2 + c9* y2 + c10* x2*y2 + c11* x2*x2 + c12* y2*y2
eq9  = - v3 + c7 + c8* x3 + c9* y3 + c10* x3*y3 + c11* x3*x3 + c12* y3*y3
eq10 = - v4 + c7 + c8* x4 + c9* y4 + c10* x4*y4 + c11* x4*x4 + c12* y4*y4
eq11 = - v5 + c7 + c8* x5 + c9* y5 + c10* x5*y5 + c11* x5*x5 + c12* y5*y5
eq12 = - v6 + c7 + c8* x6 + c9* y6 + c10* x6*y6 + c11* x6*x6 + c12* y6*y6

ans = sympy.solve((eq1,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10,eq11,eq12),\
                   c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12)
c1  =  ans[c1]
c2  =  ans[c2]
c3  =  ans[c3]
c4  =  ans[c4]
c5  =  ans[c5]
c6  =  ans[c6]
c7  =  ans[c7]
c8  =  ans[c8]
c9  =  ans[c9]
c10 = ans[c10]
c11 = ans[c11]
c12 = ans[c12]
u = c1 + c2*x + c3*y +  c4*xy +  c5*x**2 +  c6*y**2
v = c7 + c8*x + c9*y + c10*xy + c11*x**2 + c12*y**2


