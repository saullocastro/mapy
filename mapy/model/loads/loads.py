import alg3dpy
from mapy.reader import user_setattr
#
class Loads(object):
    def __init__(self):
        self.subcases = {}

    def rebuild(self):
        pass

    def add2model(self, model):
        self.model = model 
        model.loadcount += 1
        self.loadcount = model.loadcount
        model.loaddict[model.loadcount] = self

    def set_subcase(self, subcase):
        self.subcases[subcase.id] = subcase
        if self.__class__.__name__.find('Load') > -1:
            for combloadid in self.loads:
                for load in self.model.loaddict.values():
                    if load.id == combloadid:
                        load.set_subcase(subcase)

    def add2grid(self):
        if self.__class__.__name__.find('Load') > -1:
            return False
        if self.__class__.__name__.find('Moment') > -1:
            ref = 3
        else:
            ref = 0
        grid = self.model.griddict[int(self.gridid)]
        for sub in self.subcases.values():
            if not sub.loadid in self.model.loaddict.keys():
                lf = 1.
            else:    
                load = self.model.loaddict[sub.loadid]
                if load.__class__.__name__.find('Load') > -1:
                    lf = load.scaledict[self.id]
                else:
                    lf = 1.
            grid.add_load(sub.id, ref + 1, lf * float(self.x1))
            grid.add_load(sub.id, ref + 2, lf * float(self.x2))
            grid.add_load(sub.id, ref + 3, lf * float(self.x3))
        return True
        
class Force(Loads):

    def __init__(self, inputs):    
        Loads.__init__(self)
        self = user_setattr(self, inputs)
        self.lf = {}
        self.lf[self.id] = 1.

    def rebuild(self):    
        if getattr(self, 'g1id', False) <> False:
            g1id = int(self.g1id)
            g2id = int(self.g2id)
            self.g1obj = self.model.griddict[g1id]
            self.g2obj = self.model.griddict[g2id] 
            self.calc_x1_x2_x3(model)
        else:
            self.x1 = float(self.f) * float(self.x1)
            self.x2 = float(self.f) * float(self.x2)
            self.x3 = float(self.f) * float(self.x3)

    def calc_x1_x2_x3(self):
        self.vec = alg3dpy.Vec(self.g1obj, self.g2obj)
        cosbeta, cosgama = self.vec.cosines_GLOBAL()
        senbeta = (1 - cosbeta**2)**0.5
        sengama = (1 - cosgama**2)**0.5
        self.x1 = float(self.f) * cosgama * cosbeta
        self.x2 = float(self.f) * sengama
        self.x3 = float(self.f) * cosgama * senbeta
        

class Moment(Loads):

    def __init__(self, inputs):    
        Loads.__init__(self)
        self = user_setattr(self, inputs)

    def rebuild(self):    
        self.x1 = float(self.f) * float(self.x1)
        self.x2 = float(self.f) * float(self.x2)
        self.x3 = float(self.f) * float(self.x3)

class Load(Loads):

    def __init__(self, inputs):    
        Loads.__init__(self)
        self = user_setattr(self, inputs)
        self.loads = [int(i) for i in self.loads]
        self.scales = [float(i) for i in self.scales]
        self.scale_overall = float(self.scale_overall)

    def rebuild(self):    
        self.scaledict = {}
        for i in xrange(len(self.loads)):
            self.scaledict[self.loads[i]] = self.scales[i] * self.scale_overall
#        self.combload = {}
#        for i in xrange(len(self.loads)):
#            load = int(self.loads[i])
#            scale = float(self.scales[i])
#            self.combload[load] = self.model.loaddict[load]
#            self.combload[load].lf[self.id] = self.scale_overall * self.scale
            
            
