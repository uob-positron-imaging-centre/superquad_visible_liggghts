
from math import sqrt
def print_bug(msg,debug):
    if debug:
        print_bug(msg)
debug = False
input1 = self.GetInputDataObject(0, 0)
input2 = self.GetInputDataObject(0, 1)
output = self.GetOutputDataObject(0)
newPoints = vtk.vtkPoints()
newcells = vtk.vtkCellArray()
#
P=input1.GetPointData()
B=input2.GetPointData()
BODIES=input1.GetNumberOfPoints() #number of particles in vtk file
EDGES=input2.GetNumberOfPoints()    #edges for the superquadric
SURFACES=input2.GetNumberOfCells()  #surfaces of the superquadric
# define the output (should set to vtkunstructuredgrid)
outputarrayID = vtk.vtkDoubleArray()
outputarrayID.SetName("ID")
outputarrayID.SetNumberOfTuples(BODIES*SURFACES)
#
outputarrayT = vtk.vtkDoubleArray()
outputarrayT.SetName("type")
outputarrayT.SetNumberOfTuples(BODIES*SURFACES)
#
#outputarraySC = vtk.vtkDoubleArray()
#outputarraySC.SetName("value")
#outputarraySC.SetNumberOfTuples(BODIES*SURFACES)
#
outputarrayF = vtk.vtkDoubleArray()
outputarrayF.SetName("f")
outputarrayF.SetNumberOfTuples(BODIES*SURFACES)
#
outputarray_v = vtk.vtkDoubleArray()
outputarray_v.SetName("v")
outputarray_v.SetNumberOfTuples(BODIES*SURFACES)
k=0
c=0
print_bug(f"Number of particles: {BODIES}",debug)
for body in range(0,BODIES): # for each particle
    r=input1.GetPoint(body)
    M=P.GetAbstractArray('TENSOR')
    T11=M.GetComponent(body,0)

    T12=M.GetComponent(body,1)
    T13=M.GetComponent(body,2)
    T21=M.GetComponent(body,3)
    T22=M.GetComponent(body,4)
    T23=M.GetComponent(body,5)
    T31=M.GetComponent(body,6)
    T32=M.GetComponent(body,7)
    T33=M.GetComponent(body,8)
    type=P.GetArray('type').GetValue(body)-1
    CLUMP_ID=P.GetArray("id").GetValue(body);
    #CLUMP_SC=P.GetArray("value").GetValue(body);
    CLUMP_FORCEx=P.GetAbstractArray("f").GetComponent(body,0)
    CLUMP_FORCEy=P.GetAbstractArray("f").GetComponent(body,1)
    CLUMP_FORCEz=P.GetAbstractArray("f").GetComponent(body,2)
    CLUMP_FORCE=sqrt(CLUMP_FORCEx*CLUMP_FORCEx+CLUMP_FORCEy*CLUMP_FORCEy+CLUMP_FORCEz*CLUMP_FORCEz)
    CLUMP_VELx=P.GetAbstractArray("v").GetComponent(body,0)
    CLUMP_VELy=P.GetAbstractArray("v").GetComponent(body,1)
    CLUMP_VELz=P.GetAbstractArray("v").GetComponent(body,2)
    CLUMP_VEL=sqrt(CLUMP_VELx*CLUMP_VELx+CLUMP_VELy*CLUMP_VELy+CLUMP_VELz*CLUMP_VELz)
    print_bug(f"Number of Surfaces: {SURFACES}", debug)
    for surface in range(0,SURFACES):
        outputarrayID.SetValue(k,CLUMP_ID)
        outputarrayT.SetValue(k,type)
        outputarrayF.SetValue(k,CLUMP_FORCE)
        #outputarraySC.SetValue(k,CLUMP_SC)
        outputarray_v.SetValue(k,CLUMP_VEL)
        k+=1
        cell = input2.GetCell(surface)
        COUNT=cell.GetNumberOfPoints()
        print_bug(f"c before is : {c}",debug)
        c_old =c
        for j in range(0,COUNT): #alle punkte der jeweiligen zelle
            id=cell.GetPointId(j)
            #print id
            coord = input2.GetPoint(id)
            x, y, z = coord[:3]
            #print x,y,z
            #print r
            xnew=T11*x+T12*y+T13*z+r[0]
            ynew=T21*x+T22*y+T23*z+r[1]
            znew=T31*x+T32*y+T33*z+r[2]
            newPoints.InsertPoint(c, xnew, ynew, znew)
            c+=1
        #print_bug("c after is : ",c)
        #print_bug("c diff is : ",-c_old +c)
        newcells.InsertNextCell(6)
        newcells.InsertCellPoint(c-1)
        newcells.InsertCellPoint(c-2)
        newcells.InsertCellPoint(c-3)
        newcells.InsertCellPoint(c-4)
        #print_bug("Surface number is: ",surface," Max Surface: ",SURFACES)
        newcells.InsertCellPoint(c-5)
        newcells.InsertCellPoint(c-6)
output.SetPoints(newPoints)
output.SetCells(6,newcells)
output.GetCellData().AddArray(outputarrayID)
output.GetCellData().AddArray(outputarrayT)
output.GetCellData().AddArray(outputarrayF)
#output.GetCellData().AddArray(outputarraySC)
output.GetCellData().AddArray(outputarray_v)
