import numpy as np
import sympy
from sympy import Matrix, integrate, simplify

def mintegrate(m, var, l1, l2, mname, sufix, norm=False):
    print '\tstarting integration of {mname} over {var}'.format(
            mname=mname, var=var)
    m = Matrix(m)
    sympy.var('AAA')
    if norm:
        # changing variables
        subs = {var: (l2-l1)*AAA + l1}
        m = m.subs(subs)
        m *= (l2-l1)
    # integration
    for (i, j), ki in np.ndenumerate(m):
        if norm:
            ki = integrate(ki, (AAA, 0, 1), conds='none')
        else:
            ki = integrate(ki, (var, l1, l2), conds='none')
        print '\tfinished integrate {mname}_{sufix}[{i}, {j}] over {var}'.\
                format(mname=mname, sufix=sufix, i=i, j=j, var=var)
        m[i, j] = ki
    for (i, j), ki in np.ndenumerate(m):
        ki = simplify(ki)
        print '\tfinished simplify {mname}_{sufix}[{i}, {j}] over {var}'.\
                format(mname=mname, sufix=sufix, i=i, j=j, var=var)
        m[i, j] = ki
    # printing
    filename = 'print_{mname}_{sufix}_over_{var}.txt'.format(
            mname=mname, sufix=sufix, var=var)
    with open(filename, 'w') as f:
        def myprint( sth ):
            f.write( str(sth).strip() + '\n' )
        myprint('matrix ' + mname + ' in file ' + filename)
        for (i, j), v in np.ndenumerate(m):
            if v:
                myprint(mname + '[{0},{1}] = {2}'.format(i,j,v))
    return m

def dbl_mintegrate(m, a, a1, a2, b, b1, b2, mname, sufix,
        norm1=False, norm2=False):
    m = mintegrate(m, a, a1, a2, mname, sufix, norm=norm1)
    m = mintegrate(m, b, b1, b2, mname, sufix, norm=norm2)
    return m

def mprint_mathematica(m, mname, sufix):
    from mathematica_printer import print_mathematica
    filename = 'print_mathematica_{0}_{1}.txt'.format(mname, sufix)
    with open(filename, 'w') as f:
        f.write(print_mathematica(m) + '\n')
