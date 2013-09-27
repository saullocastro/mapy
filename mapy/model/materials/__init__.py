# 
class Materials(object):
    def __init__( self ):
        pass
    def add2model( self, model ):
        self.model = model
        model.matdict[self.id] = self
