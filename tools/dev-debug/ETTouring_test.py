import sys
sys.path.append('../ree/tools')
import EFormatConverters as ET
import EFormatGraph
import os
import icing
from datetime import datetime
import copy
import eminipyparser

teststr1 = r'''
find b : bool such that b = exists i : int(0..4) . i*i=i
'''
teststr1 = r'''
letting a be true
letting b be false
find c : int(0..10)
such that
   c = 2* (toInt(a\/b/\(a \/ false))+2)
'''

teststr2 = r'''
$ graph multicolouring for directed graphs
$ uses exactly coloursPerNode colours for each vertex
given n : int(1..100)
letting vertices be domain int(1..n)
given edges : relation (irreflexive) of ( vertices * vertices )
given numberColours : int(1..n)
given coloursPerNode : int(1..numberColours)
letting colours be domain int(1..numberColours)
find c : relation (size n*coloursPerNode) of ( vertices * colours )
such that true

$ endpoints of edges do not share colours
,  forAll (u,v) in edges .
      (forAll colourAssignment in c .
         (colourAssignment[1] = u) -> !((v,colourAssignment[2]) in c))

$ enforce number of colours per node, another version
,  forAll u in vertices .
      coloursPerNode = sum colourAssignment in c .
         toInt(colourAssignment[1] = u)
'''

teststr0 = r'''
find s : int(1..200)
such that s = (5+
, s = 15
'''
teststr0 = r'''
letting a be domain int(0..10)
find g: relation (minSize 10, maxSize 20, irreflexive) of (a*a)
such that
   5 = 3+2
'''

#with open('tests/treeGen.essence', 'r') as file:
#      teststr0 = file.read()
print(teststr2)
teststr = copy.deepcopy(teststr2)
ast = ET.EminiToASTpy(teststr)

ET.ep.printTree(ast, printInfo=True)

emini = ET.ASTpyToEmini(ast)
ETG = EFormatGraph.ETGraph()
print(emini)
emini2 = copy.deepcopy(teststr)
works = True
for i in range(0,1):
    print("TOUR Starts")
    results = ETG.heuristicChinesePostman(emini2,"Emini")
    #print(results)
    works = (works and results[0] == emini)
    if not works:
        print(results[0])
print("String equality")
print(works)

ast2 = ET.EminiToASTpy(results[0])
print("tree equality")
print(eminipyparser.treeEquality(ast,ast2))


