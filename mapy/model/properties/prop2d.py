from mapy.reader import user_setattr
from mapy.model.properties import Properties
#
class Prop2D(Properties):

    def __init__(self):
        super( Prop2D, self ).__init__()

class PropShell(Prop2D):

    def __init__(self, inputs):    
        super( PropShell, self).__init__()
        self = user_setattr(self, inputs)

    def build_C(self):
        import scipy
        Emat = self.matobj.e
        if self.matobj.nu:
            Gmat = Emat/(2.*(1+self.matobj.nu))
        else:
            Gmat = self.matobj.g
            self.matobj.nu = Emat/Gmat/2. - 1
        nu   = self.matobj.nu
        self.C = (Emat/(1-nu**2)) * scipy.array([\
                     [ 1 , nu ,        0],\
                     [nu ,  1 ,        0],\
                     [0  ,  0 , (1-nu)/2]])

