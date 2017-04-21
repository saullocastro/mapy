import time
from mapy.constants import CSYSGLOBAL

def get_cons(grid, sub_id):
    if sub_id in grid.cons.keys():
        if len(grid.perm_cons) > 0:
            cons = list(grid.perm_cons | grid.cons[sub_id])
        else:
            cons = list(grid.cons[sub_id])
    else:
        cons = list(grid.perm_cons)
    cons.sort()
    return cons

#TODO  para encontrar elementos / nos mais proximos
#
#TODO
# cria classe cubos
# determinados em funcao das coordenadas min e max do modelos
# cada cubo leva a lista dos elementos que serao considerados nas varreduras
# cada cubo tem os atributos xmin xmax ymin ymax zmin zmax

#TODO
# varredura direcional obtendo-se os elementos adjacentes e escolhendo qual
# direcao e melhor no sentido de reduzir a distancia
#



class Model(object):

    __slots__ = [ 'name','coorddict','griddict','elemdict','matdict',
                  'propdict','loaddict','loadcount','consdict','conscount',
                  'subcases','k_pos','k_offset','index_to_delete','k_coo',
                  'k_coo_sub','F','fv' ]

    def __init__(self, name='default_name'):
        self.name = name
        self.coorddict = {}
        self.griddict = {}
        self.elemdict = {}
        self.matdict = {}
        self.propdict = {}
        self.loaddict = {}
        self.loadcount = 0
        self.consdict = {}
        self.conscount = 0
        self.subcases = {}
        self.k_pos = None
        self.k_offset = None
        self.index_to_delete = None
        self.k_coo = None
        self.k_coo_sub = {}
        self.F = {}
        self.fv = None
        CSYSGLOBAL.model = self
        self.coorddict[0] = CSYSGLOBAL

    def add_subcase(self, id, loadid, consid):
        import loads
        self.subcases[int(id)] = loads.Subcase(id, loadid, consid)
        self.subcases[int(id)].model = self

    def rebuild(self):
        """
        Add direct object references for all entries

        Grids <--> CoordSys loops. They are processed in the following order:
            - basic grids and the basic coord sys
            - grids depending on the basic coord sys
            loop:
                - coord sys depending on these grids
                - grids depending on these coord sys
            until all grids and coordsys are processed
        ERRORS:
            - Grids that make reference to an unexisting coordsys
            - CoordSys that make reference to an unexisting grid
        DEFINITIONS:
            - basic coord sys are those created from vectors which are
              defined in the basic coordinate system (id=0),
              or those which g1, g2 and g3 are basic grids
            - basic grids are those making reference to the basic
              coordinate system (id=0)
        """
        import rebuild
        rebuild.rebuild( self )

    def build_k(self):
        '''
        Build the global stiffness matrix
        '''
        print(time.ctime() + ' started  - building grid positions in global stiffness matrix')
        self.build_k_pos()
        print(time.ctime() + ' finished - building grid positions in global stiffness matrix')
        print(time.ctime() + ' started  - building lists of constraints')
        self.build_index_to_delete()
        print(time.ctime() + ' finished - building lists of constraints')
        print(time.ctime() + ' started  - building global K stiffness matrix')
        self.build_k_coo()
        self.build_k_coo_sub()
        print(time.ctime() + ' finished - building global K stiffness matrix')
        print(time.ctime() + ' started  - building global F load matrices')
        self.build_F()
        print(time.ctime() + ' finished - building global F load matrices')


    def build_k_pos(self):
        pos = -1
        k_pos = []
        for elem in self.elemdict.values():
            for grid in elem.grids:
                if grid.pos == -1:
                    pos += 1
                    grid.pos = pos
                    k_pos.append( grid.id )

        k_offset = {}
        for sub in self.subcases.values():
            k_offset[sub.id] = []
            offset = 0
            for i in range(len(k_pos)):
                if i > 0:
                    gi_1_id = k_pos[ i-1 ]
                    gi_1 = self.griddict[ gi_1_id ],
                    'subcases'
                    cons = get_cons( gi_1 , sub.id )
                    offset += len( cons )
                k_offset[sub.id].append( offset )
                gi_id = k_pos[ i ]
                gi = self.griddict[ gi_id ]
                gi.k_offset[sub.id] = offset

        self.k_pos = k_pos
        self.k_offset = k_offset

    def build_index_to_delete(self):
        self.index_to_delete = {}
        for sub in self.subcases.values():
            index_to_delete = []
            for gid in self.k_pos:
                grid = self.griddict[gid]
                pos = grid.pos
                cons = get_cons(grid,sub.id)
                for dof in cons:
                    index_to_delete.append( pos * 6 + (dof-1) )
            index_to_delete.sort()
            self.index_to_delete[sub.id] = index_to_delete

    def build_k_coo(self):
        import scipy
        import scipy.sparse as ss
        import alg3dpy.scipy_sparse as assparse
        dim = 6 * len(self.k_pos)
        data = scipy.zeros(shape=0, dtype='float64')
        row =  scipy.zeros(shape=0, dtype='int64')
        col =  scipy.zeros(shape=0, dtype='int64')
        for elem in self.elemdict.values():
            elem.build_k()
            for i in range(len(elem.grids)):
                gi = elem.grids[i]
                for j in range(len(elem.grids)):
                    gj = elem.grids[j]
                    k_grid = assparse.in_sparse(elem.k,i*6,i*6+5,j*6,j*6+5)
                    #
                    for d, r, c, in zip(k_grid.data, k_grid.row, k_grid.col):
                        newr = r + gi.pos * 6
                        newc = c + gj.pos * 6
                        data = scipy.append(data, d   )
                        row  = scipy.append(row , newr)
                        col  = scipy.append(col , newc)
        k_coo = ss.coo_matrix(( data, (row,col) ), shape=(dim,dim))
        self.k_coo = k_coo

    def build_k_coo_sub(self):
        #FIXME if this will be kept... optimize.. there are too many loops
        #TOOOOOO SLOW
        self.k_coo_sub = {}
        for sub in self.subcases.values():
            k = self.k_coo
            count = -1
            for row, col, in zip( k.row, k.col ):
                count += 1
                for grid_id in self.k_pos:
                    grid = self.griddict[grid_id]
                    pos = grid.pos
                    cons = get_cons( grid, sub.id )
                    for i in cons:
                        j = (i - 1) + pos*6
                        if row == j or col == j:
                            if row == col:
                                k.data[count] = 1.
                            else:
                                k.data[count] = 0.
            self.k_coo_sub[sub.id] = k

    def build_F(self):
        import scipy
        self.F = {}
        for sub in self.subcases.values():
            dim = self.k_coo_sub[sub.id].shape[1]
            self.F[sub.id] = scipy.zeros(shape=dim, dtype='float64')
        for gid in self.k_pos:
            grid = self.griddict[gid]
            grid_load = grid.loads
            for sub in self.subcases.values():
                if sub.id in grid_load.keys():
                    loads = grid_load[sub.id]
                    #k_offset = grid.k_offset[sub.id]
                    #cons = get_cons(grid, sub.id)
                    #sub_i = 0
                    for i in range(6):
                        index = i + grid.pos*6
                        self.F[sub.id][index] = loads[i]

#                        if not (i+1) in cons:
#                            index = i + grid.pos*6 - k_offset - sub_i
#                            self.F[sub.id][index] = loads[i]
#                        else:
#                            sub_i += 1



    def print_displ(self, sub_id = 'all'):
        if sub_id == 'all':
            for sub in self.subcases.values():
                for grid in self.griddict.values():
                    grid.print_displ(sub.id)
        else:
            for grid in self.griddict.values():
                grid.print_displ(sub_id)

    def elem_out_vecs(self):
        for elem in self.elemdict.values():
           elem.calc_displ()
           elem.calc_out_vecs()

    def createfemview(self):
        import mapy
        self.fv = mapy.renderer.FEMView(self)


    def TOBEFIXED_build_k_coo_sub(self):
        import scipy
        import scipy.sparse as ss
        import alg3dpy.scipy_sparse as assparse
        #FIXME not considering pos to build the matrix!!!
        self.k_coo_sub = {}
        for sub in self.subcases.values():
            dim = 6*len( self.k_pos ) - \
                    len( self.index_to_delete[ sub.id ] )
            data = scipy.zeros(0, dtype='float64')
            row =  scipy.zeros(0, dtype='int64')
            col =  scipy.zeros(0, dtype='int64')
            for elem in self.elemdict.values():
                numg = len( elem.grids )
                for i in range( numg ):
                    gi = elem.grids[ i ]
                    offseti = gi.k_offset[ sub.id ]
                    consi = set( [] )
                    if sub.id in gi.cons.keys():
                        consi = gi.cons[ sub.id ]
                    for j in range( numg ):
                        gj = elem.grids[ j ]
                        offsetj = gj.k_offset[ sub.id ]
                        consj = set( [] )
                        if sub.id in gj.cons.keys():
                            consj = gj.cons[ sub.id ]
                        cons = consi | consj
                        index_to_delete = [ (c-1) for c in cons ]
                        k_grid = assparse.in_sparse(elem.k,i*6,i*6+5,j*6,j*6+5)

                        if len(index_to_delete) < 6:
                            k = k_grid
                            for d, r, c, in zip( k.data , k.row, k.col ):
                                #FIXME remove the search below
                                if not r in index_to_delete:
                                    sub_r = 0
                                    for k in index_to_delete:
                                        if r > k:
                                            sub_r += 1
                                    if not c in index_to_delete:
                                        sub_c = 0
                                        for m in index_to_delete:
                                            if c > m:
                                                sub_c += 1
                                        newr = r + gi.pos * 6 - offseti - sub_r
                                        newc = c + gj.pos * 6 - offsetj - sub_c
                                        data = scipy.append( data , d    )
                                        row  = scipy.append( row  , newr )
                                        col  = scipy.append( col  , newc )
            k_coo = ss.coo_matrix(( data, (row,col) ), shape=(dim,dim))
            self.k_coo_sub[sub.id] = k_coo
