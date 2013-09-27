import os
#import solver
class FEM(object):
    '''
    Finite Element Method class
    '''
    def __init__(self):
        pass

    def create_model(self, name='default_name'):
        self.model = model.Model( name )

    def read_new_file(self, file_path, solvername='nastran'):
        solvername = solvername.lower()
        self.file = reader.InputFile(file_path, solvername)
        model_name = os.path.basename(file_path)
        self.create_model(model_name)
        for data in self.file.data:
            outputcard = reader.card2dict(data, self.file.solvername)
            obj = outputcard['entryclass'](outputcard)
            obj.entryclass = str(obj.entryclass)
            obj.add2model(self.model)

    def solve_k_coo_sub(self):
        [full_displ, full_F] = solver.solve_k_coo_sub(self.model)
        ind = 0
        for gid in self.model.k_pos:
            grid = self.model.griddict[gid]
            for sub in self.model.subcases.values():
                displ = full_displ[sub.id][ind*6 : ind*6 + 6]
                grid.attach_displ( sub.id, displ )
            ind += 1
