from libcpp cimport bool
from cpython cimport tuple

import numpy as np
cimport numpy as np

DOUBLE = np.float64
ctypedef np.float_t cDOUBLE

#cdef extern from 'lapacke.h':
    #void LAPACK_dgelsd(int* m, int* n, int* nrhs, double* a,
                       #int* lda, double* b, int* ldb, double* s,
                       #double* rcond, int* rank, double* work,
                       #int* lwork, int* iwork, int *info);
    #int LAPACK_ROW_MAJOR=101
    #int LAPACK_COL_MAJOR=102

cdef int inv(double *a, int n, int lda):
    cdef int *ipiv
    LAPACKE_dgelsd(n, n, a, lda, ipiv)

cdef polyv_lapack(void f, np.ndarray xs, int nf, int order, int fdim):
    #TODO
    cdef int nxs = xs.shape[0]
    cdef int i
    cdef np.ndarray[cDOUBLE, ndim=1] ans, xis, ais, outf
    cdef np.ndarray[cDOUBLE, ndim=2] X, outf_all
    cdef double xi
    outf_all = np.zeros((npts, fdim), dtype=DOUBLE)
    ans = np.zeros(nf, dtype=DOUBLE)
    xis = np.zeros(order+1, dtype=DOUBLE)
    X = np.zeros((order+1, order+1), dtype=DOUBLE)
    outf = np.zeros(fdim, dtype=DOUBLE)
    if nxs % (npts+1) != 0:
        raise ValueError('poly: The size of xs must be a multiple of "npts+1"')
    for i in range(0, nxs, npts):
        for j in range(1, npts+1):
            xi = xs[i-order+j]
            for k in range(order+1):
                X[j,k] = xi**k
            f(xi, outf)
            ais = np.asarray( np.dot( inv(X), tmp.transpose() ) )
        for k in range(1, order+2):
            ans += ais[k-1,:]/k * (xis[-1]**k - xis[0]**k)
    return ans

