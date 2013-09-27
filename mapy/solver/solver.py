import numpy as np
import time
import scipy
import scipy.sparse as ss
import scipy.sparse.linalg as linalg

def solve_k_coo_sub(model):
    full_displ = {}
    full_F = {}
    for sub in model.subcases.values():
        #        
        F = model.F[sub.id]
        #
        K = model.k_coo_sub[sub.id]
        #
        x = linalg.spsolve( K.tocsc(), F )
        #
        index_to_zero = model.index_to_delete[sub.id]        
        #for i in index_to_zero:
        #    if i > len(x):
        #        i = len(x)
        #    x = scipy.insert( x , i , 0. )
        full_displ[sub.id] = x
        full_F[sub.id] = np.dot( model.k_coo, x )

    return [full_displ, full_F]

