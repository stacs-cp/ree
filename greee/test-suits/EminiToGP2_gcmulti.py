import sys
sys.path.append('.')

from greee import EFormatGraph



gcmulti = r'''
given n : int(1..100)
letting vertices be domain int(0..n-1)
given edges : relation (irreflexive) of ( vertices * vertices )
given numberColours : int(1..n)
given coloursPerNode : int(1..n)
letting colours be domain int(1..numberColours)
find c : relation (size n*coloursPerNode) of ( vertices * colours )
such that true

$ endpoints of edges do not share colours
,  forAll (u,v) in edges .
      (forAll colourAssignment in c .
         (colourAssignment[1] = u) -> !((v,colourAssignment[2]) in c))

$ enforce number of colours per node, another version
,  forAll u : vertices .
      coloursPerNode = (sum colourAssignment in c .
         toInt(colourAssignment[1] = u))
'''
EFG = EFormatGraph.EFGraph()
gp2str = EFG.FormToForm(gcmulti, "Emini","GP2String")
hostFileName = "gp2/gcmulti.host"
with open(hostFileName, 'w') as file:
    file.write(gp2str)

gcmultifunc = r'''
given n : int(0..100)
letting vertices be domain int(0..n-1)
given edges : relation (irreflexive) of ( vertices * vertices )
given numberColours : int(1..n)
given coloursPerNode : int(1..n)
letting colours be domain int(1..numberColours)
letting coloursSet be domain set (size coloursPerNode) of colours
find c : function (total) vertices --> coloursSet
such that
forAll (u,v) in edges .
      c(v) intersect c(u) = {}'''
EFG = EFormatGraph.EFGraph()
gcmultifunc = EFG.FormToForm(gcmultifunc, "Emini","GP2String")
hostFileName2 = "gp2/gcmulti-func.host"
with open(hostFileName2, 'w') as file:
    file.write(gcmultifunc)
