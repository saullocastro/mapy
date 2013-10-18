import numpy as np
import sympy
from sympy import Matrix, integrate, simplify, trigsimp

def mintegrate(m, var, l1, l2, mname, sufix, norm=False):
    print('\tstarting integration of {mname} over {var}'.format(
            mname=mname, var=var))
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
        print('\tfinished integrate {mname}_{sufix}[{i}, {j}] over {var}'.\
                format(mname=mname, sufix=sufix, i=i, j=j, var=var))
        m[i, j] = ki
    for (i, j), ki in np.ndenumerate(m):
        try:
            ki = trigsimp(ki)
        except:
            print('\t\ttrigsimp failed {mname}_{sufix}[{i}, {j}] over {var}'.\
                format(mname=mname, sufix=sufix, i=i, j=j, var=var))
            ki = simplify(ki)
        print('\tfinished simplify {mname}_{sufix}[{i}, {j}] over {var}'.\
                format(mname=mname, sufix=sufix, i=i, j=j, var=var))
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

def mprint(m, mname, sufix):
    with open('print_{mname}_{sufix}.txt'.format(
        mname=mname, sufix=sufix), 'w') as f:
        def myprint( sth ):
            f.write( str(sth).strip() + '\n' )
        myprint('{mname}_{sufix}'.format(mname=mname, sufix=sufix))
        for (i, j), v in np.ndenumerate(m):
            if v:
                myprint('{mname}[row+{i},col+{j}] += {v}'.format(
                    mname=mname, v=v, i=i, j=j))

def mprint_as_sparse(m, mname, sufix, use_cse=False):
    if use_cse:
        subs, m_list = sympy.cse(m)
        for i, v in enumerate(m_list):
            m[i] = v

    with open('print_{mname}_{sufix}.txt'.format(mname=mname,
                                                 sufix=sufix), 'w') as f:
        def myprint( sth ):
            f.write( str(sth).strip() + '\n' )
        if use_cse:
            myprint('cdefs')
            num = 10
            for i, sub in enumerate(subs[::num]):
                myprint('cdef double ' + ', '.join(
                            map(str, [j[0] for j in subs[num*i:num*(i+1)]])))
            myprint('subs')
            for sub in subs:
                myprint('{0} = {1}'.format(*sub))
        myprint('{mname}_{sufix}'.format(mname=mname, sufix=sufix))
        for (i, j), v in np.ndenumerate(m):
            if v:
                myprint('c += 1')
                myprint('{mname}r[c] = row+{i}'.format(mname=mname, i=i))
                myprint('{mname}c[c] = col+{j}'.format(mname=mname, j=j))
                myprint('{mname}v[c] += {v}'.format(mname=mname, v=v))
