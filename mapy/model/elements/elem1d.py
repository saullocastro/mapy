from mapy.model.elements import Elements
#
class Elem1D(Elements):
    '''Elem1D include methods and attributes for all one dimensional 
    elements.
    '''
    def __init__(self):
        Elements.__init__(self)

    def rebuild(self):    
        Elements.rebuild(self)
        self.grids = []
        g1 = self.model.griddict[int(self.g1)]
        g2 = self.model.griddict[int(self.g2)]
        self.grids = [g1, g2]
        self.calc_xvec()
        self.L = self.grids[0].distfrom( self.grids[1] )

        
    def calc_xvec(self):
        g1 = self.grids[0]
        g2 = self.grids[1]
        self.xvec = g2 - g1

    def calc_vecs(self):    
        self.zvec = self.xvec.cross( self.ovec ) 
        self.yvec = self.zvec.cross( self.xvec )
