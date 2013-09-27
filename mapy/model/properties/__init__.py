#
class Properties(object):

    def __init__(self):
        pass

    def rebuild(self):    
        if getattr(self, 'mid', False) <> False:
            self.matobj = self.model.matdict[int(self.mid)]
            self.build_C()    

    def add2model(self, model):    
        self.model = model
        model.propdict[self.id] = self

    def print_warning(self, lines):
        print 'WARNING: see property %d' % self.id
        for line in lines:
            print '         ' + line

    def print_error(self, lines):
        print 'ERROR  : see property %d' % self.id
        for line in lines:
            print '         ' + line

