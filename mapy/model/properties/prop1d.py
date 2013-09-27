from mapy.reader import user_setattr 
from mapy.model.properties import Properties
class Prop1D(Properties):

    def __init__(self):
        super( Prop1D, self ).__init__()

class PropRod(Prop1D):

    def __init__(self, inputs):    
        super( PropRod, self ).__init__()
        self = user_setattr(self, inputs)

    def build_C(self):
        pass


class PropBar(Prop1D):

    def __init__(self, inputs):    
        super( PropBar, self ).__init__()
        self = user_setattr(self, inputs)

    def build_C(self):    
        import numpy
        nu   = self.matobj.nu
        Emat = self.matobj.e
        A    = self.a
        if nu:
            Gmat = Emat/(2.*(1+nu))
        else:
            Gmat = self.matobj.g
            self.matobj.nu = Emat/Gmat/2. - 1
        self.G = Gmat
        #FIXME these k below are valid for rectangular sections only
        kxy = 5/6.
        kxz = 5/6.
        GA = Gmat*A
        self.C = A*numpy.array([\
           [ Emat ,    0   , 0     ],\
           [    0 , GA*kxy , 0     ],\
           [    0 ,    0   , GA*kxz]]) 

