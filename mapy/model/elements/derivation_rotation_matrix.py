import sympy
from sympy import Matrix
sympy.var(' cosa cosb cosg sina sinb sing ')
Ra = Matrix([[1 , 0 , 0],
             [0 ,cosa,sina],
	     [0,-sina,cosa]])
Rb = Matrix([[cosb, 0,-sinb],
            [0  ,  1,  0  ],
	    [sinb,0,cosb ]])
Rg = Matrix([[cosg, sing, 0],
             [-sing,cosg,0],
	     [0,0,1]])
Rab = Ra*Rb	     
Rabg = Rab*Rg
print 'Rab',Rab
print 'Rabg',Rabg

