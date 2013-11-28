import numpy as np
import sympy
from sympy import Matrix

from mapy.sympytools.matrixtools import vdiff

def test_00():
    from sympy.abc import a, b, c, x
    A11 = x*a*c**2
    A12 = x**2*a*b*c
    A13 = x**2*a**3*b**5
    A21 = x**3*a**2*b*c
    A22 = x**4*a*b**2*c**5
    A23 = 5*x**4*a*b**2*c
    A31 = x**4*a*b**2*c**4
    A32 = 4*x**4*a*b**2*c**2
    A33 = 4*x**4*a**5*b**2*c
    A = np.array([[A11, A12, A13],
                  [A21, A22, A23],
                  [A31, A32, A33]])
    v = np.array([a, b, c])
    F = (v.T.dot(A)).dot(v)
    Av = vdiff(A, v)
    p1 = v.dot(A)
    p2 = A.dot(v)
    p3 = v.dot(Av.dot(v))
    new = p1 + p2 + p3
    ref = np.array([F.diff(a), F.diff(b), F.diff(c)])
    assert sum(sympy.simplify(Matrix(ref-new)))==0
    print('test_00 passed!')

def test_01():
    from sympy.abc import a, b, c, x
    sympy.var('c1, c2')
    A11 = x*a*c**2
    A12 = x**2*a*b*c
    A13 = x**2*a**3*b**5
    A21 = x**3*a**2*b*c
    A22 = x**4*a*b**2*c**5
    A23 = 5*x**4*a*b**2*c
    A = np.array([[A11, A12, A13],
                  [A21, A22, A23]])
    v = np.array([a, b, c])
    cc = np.array([c1, c2])
    F = cc.dot(A.dot(v))
    ref = np.array([F.diff(a), F.diff(b), F.diff(c)])
    Av = vdiff(A, v)
    p1 = cc.dot(A)
    p2 = cc.dot(Av.dot(v))
    new = p1 + p2
    assert sum(sympy.simplify(Matrix(ref-new)))==0
    print('test_01 passed!')


if __name__ == '__main__':
    test_00()
    test_01()
