from mapy.model.properties.prop2d import Prop2D
class PropShellComp(Prop2D):

    __slots__ = [ 'card', 'entryclass', 'id', 'z0', 'nsm', 'sbmat', 'ft',
                  'tref', 'dampc', 'lam', 'midlist', 'tlist', 'thetalist',
                  'laminate' ]

    def __init__(self, inputs):    
        super( PropShellComp, self ).__init__()
        self.card = None
        self.entryclass = None
        self.id = None
        self.z0 = None
        self.nsm = None
        self.sbmat = None
        self.ft = None
        self.tref = None
        self.dampc = None
        self.lam = None
        self.midlist = []
        self.tlist = []
        self.thetalist = []
        self = user_setattr(self, inputs)

