from mapy.fem import FEM

def test():
    fem = FEM()
    fem.read_new_file('dummy_wing_metallic.bdf')

if __name__ == '__main__':
    test()


