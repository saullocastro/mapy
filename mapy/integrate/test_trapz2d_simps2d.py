import numpy as np
import pyximport; pyximport.install()
import sympy
from sympy import Matrix, lambdify, cos, sin

from integratev import trapz2d, simps2d

sympy.var('x, y')
m1 = Matrix([[    x*y,    x*y**2,    x*y**3 ],
             [ x**2*y, x**2*y**2, x**2*y**3 ],
             [ x**3*y, x**3*y**2, x**3*y**3 ]])
func1 = lambdify((x,y), m1)

m2 = Matrix([[    x*cos(y),    x*cos(y)**2, x*cos(y)**2*sin(y) ],
             [ x**2*cos(y), x**2*sin(y)**2,     x**2*sin(y)**3 ],
             [ x**3*cos(y), x**3*cos(y)**2,     x**3*sin(y)**3 ]])
func2 = lambdify((x,y), m2)

def func3(x,y):
    from numpy import sin, cos
    return np.array([
        [[    x*y,    x*y**2,    x*y**3 ],
         [ x**2*y, x**2*y**2, x**2*y**3 ],
         [ x**3*y, x**3*y**2, x**3*y**3 ]],
        [[    x*cos(y),    x*cos(y)**2, x*cos(y)**2*sin(y) ],
         [ x**2*cos(y), x**2*sin(y)**2,     x**2*sin(y)**3 ],
         [ x**3*cos(y), x**3*cos(y)**2,     x**3*sin(y)**3 ]]
                    ])

def func1b(x,y,out,alpha,beta):
    out *= beta
    out += alpha*np.array([[    x*y,    x*y**2,    x*y**3 ],
                           [ x**2*y, x**2*y**2, x**2*y**3 ],
                           [ x**3*y, x**3*y**2, x**3*y**3 ]])

def func2b(x, y, out, alpha, beta):
    from numpy import sin, cos
    out *= beta
    out += alpha*np.array(
            [[    x*cos(y),    x*cos(y)**2, x*cos(y)**2*sin(y) ],
             [ x**2*cos(y), x**2*sin(y)**2,     x**2*sin(y)**3 ],
             [ x**3*cos(y), x**3*cos(y)**2,     x**3*sin(y)**3 ]])

def func3b(x,y,out,alpha,beta):
    from numpy import sin, cos
    out *= beta
    out += alpha*np.array([
        [[    x*y,    x*y**2,    x*y**3 ],
         [ x**2*y, x**2*y**2, x**2*y**3 ],
         [ x**3*y, x**3*y**2, x**3*y**3 ]],
        [[    x*cos(y),    x*cos(y)**2, x*cos(y)**2*sin(y) ],
         [ x**2*cos(y), x**2*sin(y)**2,     x**2*sin(y)**3 ],
         [ x**3*cos(y), x**3*cos(y)**2,     x**3*sin(y)**3 ]]])

if __name__ == '__main__':
    m = 100
    n = 100
    print('Testing func1:')
    print(m1)
    print('exact:')
    print(sympy.integrate(m1,(x,0.,20.),(y,-5,5)))
    print('trapz2d:')
    print(trapz2d(func1,0.,20.,m,-5,5,n))
    print('simps2d:')
    print(simps2d(func1,0.,20.,m,-5,5,n))

    print('Testing func2')
    print(m2)
    print('exact:')
    print(sympy.integrate(m2,(x,0.,20.),(y,-5,5)))
    print('trapz2d:')
    print(trapz2d(func2,0.,20.,m,-5,5,n))
    print('simps2d:')
    print(simps2d(func2,0.,20.,m,-5,5,n))

    print('Testing func3')
    print('trapz2d:')
    print(trapz2d(func3,0.,20.,m,-5,5,n))
    print('simps2d:')
    print(simps2d(func3,0.,20.,m,-5,5,n))

    print('Testing func1b:')
    print('trapz2d:')
    out = np.zeros((3,3))
    trapz2d(func1b,0.,20.,m,-5,5,n,out=out)
    print(out)
    print('simps2d:')
    out = np.zeros((3,3))
    simps2d(func1b,0.,20.,m,-5,5,n,out=out)
    print(out)

    print('Testing func2b')
    print('trapz2d:')
    out = np.zeros((3,3))
    trapz2d(func2b,0.,20.,m,-5,5,n,out=out)
    print(out)
    print('simps2d:')
    out = np.zeros((3,3))
    simps2d(func2b,0.,20.,m,-5,5,n,out=out)
    print(out)

    print('Testing func3b')
    print('trapz2d:')
    out = np.zeros((2,3,3))
    trapz2d(func3b,0.,20.,m,-5,5,n,out=out)
    print(out)
    print('simps2d:')
    out = np.zeros((2,3,3))
    simps2d(func3b,0.,20.,m,-5,5,n,out=out)
    print(out)
