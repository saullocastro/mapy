from mapy.reader import user_setattr
#
class SPC(object):

    __slots__ = ['card','entryclass','id','gridid','dof','displ','g2',
                 'c2','d2','model','conscount']

    def __init__(self, inputs):    
        self.card = None
        self.entryclass = None
        self.id = None
        self.gridid = None
        self.dof = None
        self.displ = None
        self.g2 = None
        self.c2= None
        self.d2 = None
        self.model = None
        self.conscount = None
        self = user_setattr(self, inputs)
        if self.dof.__class__.__name__ <> 'list':
            str_dof = self.dof
            self.dof = set([int(dof) for dof in str_dof])
    
    def add2model(self, model):
        self.model = model
        model.conscount += 1
        self.conscount = model.conscount
        model.consdict[model.conscount] = self
        #FIXME if g2 , c2 and d2 are given, nothing is done...
        if self.g2:
            print 'ERROR in SPC application for grid %s!!!' \
                  % str(self.g2)

    def add2grid(self, model):
        grid = model.griddict[int(self.gridid)]
        subcase = int(self.id)
        for dof in self.dof:
            grid.add_cons(subcase, dof)

