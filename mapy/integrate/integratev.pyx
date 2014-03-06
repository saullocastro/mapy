from libcpp cimport bool
from cpython cimport tuple

import numpy as np
cimport numpy as np

from scipy.linalg import inv

DOUBLE = np.float64
ctypedef np.float_t cDOUBLE

def trapzv(f, np.ndarray xs, int nf, int dimf=1):
    cdef int nxs = xs.shape[0]
    cdef np.ndarray out = np.zeros(nf, dtype=DOUBLE)
    cdef np.ndarray tmp
    cdef double x1, x2, ndim_test
    for i in range(1,nxs):
        x1 = xs[i-1]
        x2 = xs[i]
        if dimf == 2:
            out += (np.asarray(f(x2))[-1]+np.asarray(f(x1))[-1])*(x2-x1)/2.
        elif dimf == 1:
            out += (f(x2)+f(x1))*(x2-x1)/2.
        else:
            raise NotImplementedError('poly: The maximum ndim for the vector-valued function is 2')
    return out

def polyv(f, np.ndarray xs, int nf, int order=2, int dimf=1):
    cdef int nxs = xs.shape[0]
    cdef int i
    cdef np.ndarray out = np.zeros(nf, dtype=DOUBLE)
    cdef np.ndarray xis = np.zeros(order+1, dtype=DOUBLE)
    cdef np.ndarray ais
    cdef double xi
    if nxs % (order+1) != 0:
        raise ValueError('poly: The size of xs must be a multiple of "order+1"')
    for i in range(order, nxs, order):
        xis = xs[i-order:i+1]
        X = np.concatenate([(xis**i)[:,None] for i in range(order+1)], axis=1)
        if dimf == 2:
            tmp = np.concatenate([f(xi).T for xi in xis],  axis=1)
        elif dimf == 1:
            tmp = f(xis)
        else:
            raise NotImplementedError('poly: The maximum ndim for the vector-valued function is 2')
        ais = np.asarray( np.dot( inv(X), tmp.transpose() ) )
        for k in range(1, order+2):
            out += ais[k-1,:]/k * (xis[-1]**k - xis[0]**k)
    return out

def trapz2d(f, double xmin, double xmax, int m,
                double ymin, double ymax, int n,
                np.ndarray out=None, tuple args=()):
    return _trapz2d(f, xmin, xmax, m, ymin, ymax, n, out, args)

def simps2d(f, double xmin, double xmax, int m,
                double ymin, double ymax, int n,
                np.ndarray out=None, tuple args=()):
    return _simps2d(f, xmin, xmax, m, ymin, ymax, n, out, args)

cdef _trapz2d(f, double xmin, double xmax, int m,
                double ymin, double ymax, int n,
                np.ndarray out, tuple args):
    '''Integrate `f` for two variables
    This function must return a np.ndarray.
    FIXME

    '''
    cdef np.ndarray[double, ndim=1] xs, ys
    cdef int i,j
    cdef double c

    xs = np.linspace(xmin, xmax, m+1)
    ys = np.linspace(ymin, ymax, n+1)

    hx = (xmax-xmin)/m
    hy = (ymax-ymin)/n
    c = 1/4.*hx*hy

    if out is None:
        # first dummy evaluation
        out = f(xmin, ymin, *args)
        out.fill(0.)
        #
        if not isinstance(out, np.ndarray):
            raise ValueError('If `out=None`, the supplied function must ' +
                             'return a np.ndarray')
        for i,j in ( (0,0), (m,0), (0,n), (m,n) ):
            out += f(xs[i], ys[j], *args)
        for i in range(1,m): # i from 1 to m-1
            for j in (0, n):
                out += 2 * f(xs[i], ys[j], *args)
        for i in (0, m):
            for j in range(1,n): # j from 1 to n-1
                out += 2 * f(xs[i], ys[j], *args)
        for i in range(1,m): # i from 1 to m-1
            for j in range(1,n): # j from 1 to n-1
                out += 4 * f(xs[i], ys[j], *args)
        out *= c
        return out
    else:
        if not isinstance(out, np.ndarray):
            raise ValueError('The supplied `out` must be a np.ndarray')
        for i,j in ( (0, 0), (m, 0), (0, n), (m, n) ):
            f(xs[i], ys[j], out=out, alpha=1*c, beta=1, *args)
        for i in range(1, m): # i from 1 to m-1
            for j in (0, n):
                f(xs[i], ys[j], out=out, alpha=2*c, beta=1, *args)
        for i in (0, m):
            for j in range(1, n): # j from 1 to n-1
                f(xs[i], ys[j], out=out, alpha=2*c, beta=1, *args)
        for i in range(1, m): # i from 1 to m-1
            for j in range(1, n): # j from 1 to n-1
                f(xs[i], ys[j], out=out, alpha=4*c, beta=1, *args)
        return 0

cdef _simps2d(f, double xmin, double xmax, int m,
                double ymin, double ymax, int n,
                np.ndarray out, tuple args):
    '''Integrate `f` for two variables
    This function must return a np.ndarray.

    '''
    cdef np.ndarray[double, ndim=1] xs, ys
    cdef int i,j
    cdef double c

    try:
        assert m%2==0
    except AssertionError:
        print 'WARNING - incrementing m+=1'
        m += 1
    try:
        assert n%2==0
    except AssertionError:
        print 'WARNING - incrementing n+=1'
        n += 1
    m /= 2
    n /= 2

    xs = np.linspace(xmin, xmax, (2*m+1))
    ys = np.linspace(ymin, ymax, (2*n+1))

    hx = (xmax-xmin)/(2*m)
    hy = (ymax-ymin)/(2*n)
    c = 1/9.*hx*hy

    if out is None:
        # first dummy evaluation
        out = f(xmin, ymin, *args)
        out.fill(0.)
        if not isinstance(out, np.ndarray):
            raise ValueError('If `out=None`, the supplied function must ' +
                             'return a np.ndarray')
        #
        for i,j in ( (0,0), (2*m,0), (0,2*n), (2*m,2*n) ):
            out += f(xs[i], ys[j], *args)
        for i in (0, 2*m):
            for j in range(1, n+1):
                out += 4 * f(xs[i], ys[2*j-1], *args)
        for i in range(1, m+1):
            for j in (0, 2*n):
                out += 4 * f(xs[2*i-1], ys[j], *args)
        for i in (0, 2*m):
            for j in range(1, n):
                out += 2 * f(xs[i], ys[2*j], *args)
        for i in range(1, m):
            for j in (0, 2*n):
                out += 2 * f(xs[2*i], ys[j], *args)
        for i in range(1, m+1):
            for j in range(1, n+1):
                out += 16 * f(xs[2*i-1], ys[2*j-1], *args)
        for i in range(1, m+1):
            for j in range(1, n):
                out += 8 * f(xs[2*i-1], ys[2*j], *args)
        for i in range(1, m):
            for j in range(1, n+1):
                out += 8 * f(xs[2*i], ys[2*j-1], *args)
        for i in range(1, m):
            for j in range(1, n):
                out += 4 * f(xs[2*i], ys[2*j], *args)
        out *= c
        return out
    else:
        if not isinstance(out, np.ndarray):
            raise ValueError('The supplied `out` must be a np.ndarray')
        #
        for i,j in ( (0,0), (2*m,0), (0,2*n), (2*m,2*n) ):
            f(xs[i], ys[j], out=out, alpha=1*c, beta=1, *args)
        for i in (0, 2*m):
            for j in range(1, n+1):
                f(xs[i], ys[2*j-1], out=out, alpha=4*c, beta=1, *args)
        for i in range(1, m+1):
            for j in (0, 2*n):
                f(xs[2*i-1], ys[j], out=out, alpha=4*c, beta=1, *args)
        for i in (0, 2*m):
            for j in range(1, n):
                f(xs[i], ys[2*j], out=out, alpha=2*c, beta=1, *args)
        for i in range(1, m):
            for j in (0, 2*n):
                f(xs[2*i], ys[j], out=out, alpha=2*c, beta=1, *args)
        for i in range(1, m+1):
            for j in range(1, n+1):
                f(xs[2*i-1], ys[2*j-1], out=out, alpha=16*c, beta=1, *args)
        for i in range(1, m+1):
            for j in range(1, n):
                f(xs[2*i-1], ys[2*j], out=out, alpha=8*c, beta=1, *args)
        for i in range(1, m):
            for j in range(1, n+1):
                f(xs[2*i], ys[2*j-1], out=out, alpha=8*c, beta=1, *args)
        for i in range(1, m):
            for j in range(1, n):
                f(xs[2*i], ys[2*j], out=out, alpha=4*c, beta=1, *args)
        return 0

