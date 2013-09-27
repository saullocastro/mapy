class Subcase(object):
    def __init__(self, subid, loadid, consid):
        self.id = subid
        self.loadid = loadid
        self.consid = consid
    def rebuild(self):
        for load in self.model.loaddict.values():
            if load.id == self.loadid:
                load.set_subcase(self)



