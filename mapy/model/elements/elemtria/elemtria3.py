from mapy.model.elements.elem2d import Elem2D
from mapy.reader import user_setattr

class ElemTria3(Elem2D):
    def __init__(self, inputs):
        Elem2D.__init__(self)
        self = user_setattr(self, inputs)

    def rebuild(self):
        Elem2D.rebuild(self)
