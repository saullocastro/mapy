import os
import inspect

from mapy.fem import FEM

THIS_DIR = os.path.dirname(inspect.getfile(inspect.currentframe()))

def test():
    fem = FEM()
    fem.read_new_file(os.path.join(THIS_DIR, 'dummy_wing_metallic.bdf'))

if __name__ == '__main__':
    test()


