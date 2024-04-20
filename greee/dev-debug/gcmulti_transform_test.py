import os
import sys
sys.path.append('.')
from greee import gp2Interface
from greee import EFormatGraph

gcmulti = r'''
given n : int(1..100)
letting vertices be domain int(0..n-1)
given edges : relation (irreflexive) of ( vertices * vertices )
given numberColours : int(1..n)
given coloursPerNode : int(1..n)
letting colours be domain int(1..numberColours)
find c : relation (size n*coloursPerNode) of ( vertices * colours )
such that

$ endpoints of edges do not share colours
forAll (u,v) in edges .
      (forAll colourAssignment in c .
         (colourAssignment[1] = u) -> !((v,colourAssignment[2]) in c))

$ enforce number of colours per node, another version
,  forAll u : vertices .
      coloursPerNode = (sum colourAssignment in c .
         toInt(colourAssignment[1] = u))
'''
EFG = EFormatGraph.EFGraph()
gp2str = EFG.FormToForm(gcmulti, "Emini","GP2StringB")
hostFileName = "gp2/gcmultirel_B.host"
with open(hostFileName, 'w') as file:
    file.write(gp2str)


progName = "gcmultiRelToFunc7.gp2"

gp2Interface.compileGP2Program(progName)
#progName = "stringTest.gp2"
host = "gcmultirel_B.host"
#host = "gp2Test.host"
hostGraph = os.path.join("gp2",host)
gp2Interface.runPrecompiledProg(progName,hostGraph)

if os.path.isfile("gp2.output"):
            with open("gp2.output") as newGP2spec:
                gcmulti = newGP2spec.read()

EFG = EFormatGraph.EFGraph()
gcmultitrasnformed = EFG.FormToForm(gcmulti, "GP2StringB","Emini")
print(gcmultitrasnformed)