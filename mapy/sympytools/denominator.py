from itertools import combinations

import numpy as np

def null_denominator_conditions(variables):
    size = len(variables)
    conditions = []
    for num_of_signs in range(1, size):
        for comb in combinations(range(size), num_of_signs):
            signs = np.ones(size, dtype=int)
            signs[np.array(comb)] = -1
            cond = (signs*variables).sum()
            conditions.append(cond)

    return sorted(list(conditions), key= lambda x:str(x))


