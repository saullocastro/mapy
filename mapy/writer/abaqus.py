from abaqus import *
from abaqusConstants import *
from regionToolset import Region
def model_create( mdb, model ):
    mdb.Model( model.name)
    
class AModel(object):
    def __init__( self ):
        self.amodel = amodel



print 'CYLINDER MODULE'
backwardCompatibility.setValues(includeDeprecated=True, reportDeprecated=False)
mdb.saveAs(pathName='C:/Temp/abaqus/cylinder.cae')
#RESETING THE CURRENT VIEWPORT
myView = session.viewports[ session.currentViewportName ]
myView.setValues( displayedObject=None )
#CREATING A NEW MODEL
myMod = mdb.Model(name=MODELNAME)
#DELETING THE DEFAULT MODEL
#del mdb.models['Model-1']
#CREATING A NEW PART
partCyl = myMod.Part( name='Cylinder',
                      dimensionality=THREE_D, 
                      type=DEFORMABLE_BODY )
#CREATING AN ISOTROPIC MATERIAL
myMat = myMod.Material( name='aluminum' )
elasticProp = ( E, NU )
myMat.Elastic( table=( elasticProp , ) )
#CREATING THE PROPERTY (isotropic shell)
shellSection = myMod.HomogeneousShellSection( name='AluminumPlate',
                                             material='aluminum',
                                             thickness=T )
#CREATING THE SKETCH which will be used to create the shell geometry
s1 = myMod.ConstrainedSketch( name='SketchCylinder', 
                              sheetSize=max( [2.1*R, 1.1*H] ) )
#axis of revolution
s1.ConstructionLine( point1=(0,-H), point2=(0,H) )
#line to be revoluted
s1.Line( point1=(R,-H/2.), point2=(R,H/2.) )

#CREATING A LOCAL COORDINATE SYSTEM TO USE IN THE BOUNDARY CONDITIONS
csysCyl = partCyl.DatumCsysByThreePoints( name='CSYSCylinder',
                                          coordSysType=CYLINDRICAL,
                                          origin=(0,0,0),
                                          point1=(1,0,0),
                                          point2=(1,0,-1) )
#CREATING THE CYLINDER SHELL GEOMETRY
myCyl = partCyl.BaseShellRevolve( sketch=s1,
                                  angle=360.0,
                                  flipRevolveDirection=OFF )
#PROPERTY - assigning the property to the corresponding faces
partCyl.SectionAssignment( 
    region=Region( faces=partCyl.faces.findAt(((-R,0,0),)) ),
    sectionName='AluminumPlate' )

#DEFINING THE MESH SEEDS ALONG ALL EDGES
partCyl.PartitionEdgeByParam( edges=partCyl.edges.findAt( ((R,0,0),) ),
                              parameter=PLpoint )
partCyl.seedEdgeBySize(edges= partCyl.edges.findAt( ((R,-H/2,0),) ),
                       size=ELSIZE,
                       deviationFactor=0.1,
                       constraint=FINER)
partCyl.seedEdgeBySize(edges= partCyl.edges.findAt( ((R, H/2,0),) ),
                       size=ELSIZE,
                       deviationFactor=0.1,
                       constraint=FINER)
partCyl.seedEdgeBySize(edges= partCyl.edges.findAt( ((R,-H/4,0),) ),
                       size=ELSIZE,
                       deviationFactor=0.1,
                       constraint=FINER)
partCyl.seedEdgeBySize(edges= partCyl.edges.findAt( ((R, H/4,0),) ),
                       size=ELSIZE,
                       deviationFactor=0.1,
                       constraint=FINER)
#ASSEMBLIES adding the cylinder to assembly
instCyl = myMod.rootAssembly.Instance( name='InstanceCylinder',
                             part=partCyl,
                             dependent=ON)
#BOUNDARY CONDITIONS
localCSYS = instCyl.datums[1]
#bot boundary conditions
botEdgeArray =  instCyl.edges.findAt( ( (-R,-H/2,0 ), ) )
myMod.DisplacementBC( name='BotBC',
                      createStepName='Initial',
                      region = Region( edges=botEdgeArray ),
                      u1=UNSET,
                      u2=SET,
                      u3=SET,
                      ur1=SET,
                      ur2=UNSET,
                      ur3=UNSET,
                      amplitude = UNSET,
                      distributionType = UNIFORM,
                      fieldName = '',
                      localCsys = localCSYS,
                      #buckleCase=BUCKLING_MODES
                    ) #NOT_APPLICABLE
#top boundary conditions
topEdgeArray = instCyl.edges.findAt( ( (-R, H/2,0 ), ) )
myMod.DisplacementBC( name='TopBC',
                      createStepName='Initial',
                      region = Region( edges=topEdgeArray ),
                      u1=UNSET,
                      u2=SET,
                      u3=UNSET,
                      ur1=SET,
                      ur2=UNSET,
                      ur3=UNSET,
                      amplitude = UNSET,
                      distributionType = UNIFORM,
                      fieldName = '',
                      localCsys = localCSYS,
                      #buckleCase=BUCKLING_MODES
                    ) #NOT_APPLICABLE
#LOADS
myMod.StaticStep( name='PerturbationStep',
                  previous='Initial',
                  nlgeom=True )
#perturbation load
verticePL = instCyl.vertices.findAt( ((R, 0, 0),) )
myMod.ConcentratedForce( name='PerturbationLoad',
                         createStepName = 'PerturbationStep',
                         region= Region( vertices=verticePL ),
                         cf1 = -PLVALUE,
                         cf2 = 0.,
                         cf3 = 0. )
#axial load
topEdgeArray = instCyl.edges.findAt( ( (-R, H/2,0 ), ) )
myMod.ShellEdgeLoad(name='Load-3', 
                    createStepName='PerturbationStep',
                    region=Region( side1Edges=topEdgeArray ),
                    magnitude=AXIALLOAD, 
                    directionVector=((0.0, 0.0, 0.0), (0.0, -1.0, 0.0)), 
                    distributionType=UNIFORM,
                    field='',
                    localCsys=None,
                    traction=GENERAL, 
                    follower=OFF)
#MESHING THE PART
partCyl.generateMesh()
#CREATING JOB
job = mdb.Job( name =JOBNAME,
               model = myMod,
               scratch = r'c:\Temp\abaqus\scratch',
               memory = 4,
               memoryUnits = GIGA_BYTES,
               #numCpus = 6,
             )
job.writeInput(consistencyChecking=OFF)
mdb.save()
#: The model database has been saved to "C:\Temp\abaqus\test2.cae".
if __name__ == '__main__':
R = 50.
H = 200.
T = 2.
E = 71e3
NU = 0.33
ELSIZE = 2.
PLVALUE = 100.
PLpoint = 0.5 #cylinder height ratio
AXIALLOAD = 1000.
for i in range(10):
    PLpoint = 0.05 + 0.1*i
    JOBNAME = 'myJob_' + str(i)
    MODELNAME = 'Cylinder Model ' + str(i)
    isoCylinder( R, H, T, E, NU, 
                 ELSIZE, PLVALUE, PLpoint, AXIALLOAD, JOBNAME, MODELNAME)

    

