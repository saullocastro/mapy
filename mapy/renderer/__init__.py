import mapy
from mapy import FEM
from vtk import *
from random import random
def randomrgb():
    r = random() * 255
    g = random() * 255
    b = random() * 255
    return [r, g, b]
class FEMView(FEM):
    def __init__(self, model):
        FEM.__init__(self)
        self.points = vtkPoints()
        x1min = 1000000.
        x2min = 1000000.
        x3min = 1000000.
        x1max = 0.000001
        x2max = 0.000001
        x3max = 0.000001
        for grid in model.griddict.values():
            x1 = float(grid.x1)
            x2 = float(grid.x2)
            x3 = float(grid.x3)
            if x1 < x1min: x1min = x1
            if x2 < x2min: x2min = x2
            if x3 < x3min: x3min = x3
            if x1 > x1max: x1max = x1
            if x2 > x2max: x2max = x2
            if x3 > x3max: x3max = x3
            self.points.InsertPoint(grid.id, x1, x2, x3)
        self.quads = {}
        self.triangles = {}
        self.lines = {}
        for elem in model.elemdict.values():
            if elem.mask == True: continue
            if elem.entryclass.find('ElemQuad') > -1:
                self.quads[elem.id] = vtkQuad()
                fvelem = self.quads[elem.id]
            elif elem.entryclass.find('ElemTria') > -1:
                self.triangles[elem.id] = vtkTriangle()
                fvelem = self.triangles[elem.id]
            elif elem.entryclass.find('ElemRod') > -1:
                self.lines[elem.id] = vtkLine()
                fvelem = self.lines[elem.id]
            for i in range(len(elem.grids)):
                grid = elem.grids[i]
                fvelem.GetPointIds().SetId(i, grid.id)
        # creating actors for each model property
        self.elemArrays = {}
        self.elemPolyDatas = {}
        self.dataMappers = {}
        self.actors = {}
        self.vtkprops = {}
        for prop in model.propdict.values():
            self.elemArrays[prop.id] = vtkCellArray()
            self.elemPolyDatas[prop.id] = vtkPolyData()
            self.dataMappers[prop.id] = vtkPolyDataMapper() 
            self.actors[prop.id] = vtkActor()
            self.vtkprops[prop.id] = vtkProperty()
            elemArray = self.elemArrays[prop.id]
            elemPolyData = self.elemPolyDatas[prop.id]
            dataMapper = self.dataMappers[prop.id]
            actor = self.actors[prop.id]
            vtkprop = self.vtkprops[prop.id]
            for k in self.quads.keys():
                quad = self.quads[k]
                if model.elemdict[k].pobj.id == prop.id:
                    elemArray.InsertNextCell(quad)
            for tria in self.triangles.values():
                if tria.prop.id == prop.id:
                    elemArray.InsertNextCell(tria)
            elemPolyData.SetPoints(self.points)
            elemPolyData.SetPolys(elemArray)
            dataMapper.SetInput(elemPolyData)
            actor.SetMapper(dataMapper)
            rgb = randomrgb()
            vtkprop.SetColor(rgb)
            vtkprop.LightingOn()
            vtkprop.SetInterpolationToFlat()
            vtkprop.SetRepresentationToSurface()
            actor.SetProperty(vtkprop)
        self.render()
    def render(self):    
        self.ren = vtkRenderer()
        for actor in self.actors.values():
            self.ren.AddActor(actor)
        #self.ren.SetBackground(util.colors.slate_grey)
        self.renwin = vtkRenderWindow()
        self.renwin.AddRenderer(self.ren)
        self.renwin.SetSize(500, 500)
        style = vtkInteractorStyleTrackballCamera() 
        self.iren = vtkRenderWindowInteractor()
        self.iren.SetInteractorStyle(style) 
        self.iren.SetRenderWindow(self.renwin)
        self.iren.Initialize()
        self.renwin.Render()
        self.iren.Start()
        self.renwin.Finalize()
    def close(self):
        self.renwin.Finalize()




            



            
 
