from itertools import combinations

import numpy as np
import sympy

def null_denominator_conditions(variables):
    '''Calculate the conditions that lead to a null denominator

    The denominator is assumed to be any combinations of `variables`
    following the pattern (example with 3 variables):

    >>> v1, v2, v3 = variables
    >>> 1/(sign1*v1 + sign2*v2 + sign3*v3)

    Where `sign1` `sign2` and `sign3` can be `-1` or `+1`, and the
    conditions are obtained by swapping the signs within all possibilities.

    The conditions that are a `(-1)*` (negative) version of another are not
    returned.

    '''
    size = len(variables)
    conditions = []
    check_set = set()
    for num_of_signs in range(1, size):
        for comb in combinations(range(size), num_of_signs):
            signs = -1*np.ones(size, dtype=int)
            signs[np.array(comb)] = 1
            cond = (signs*variables).sum()
            check = sympy.solve(cond, variables[0])[0]
            if not check in check_set:
                check_set.add(check)
                conditions.append(cond)
            else:
                continue

    return conditions


