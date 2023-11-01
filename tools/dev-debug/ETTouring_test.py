import sys
sys.path.append('../ree/tools')
import EFormatConverters as ET
import EFormatGraph
import os
import icing
from datetime import datetime
import copy

teststr1 = r'''
find b : bool such that b = exists i : int(0..4) . i*i=i
'''
teststr0 = r'''
letting a be true
letting b be false
find c : int(0..10)
such that
   c = 2* (toInt(a\/b/\(a \/ false))+2)
'''

teststr1 = r'''
given a : int(0..5)
where a >2
letting n be 12
letting vertices be domain int(0..n)
find edges : relation (size n) of (vertices * vertices)
such that
forAll edge,edge2 in edges .
edge[2] > edge[1] /\
((edge != edge2) -> (edge[2] != edge2[2]))
'''

#with open('tests/treeGen.essence', 'r') as file:
#      teststr0 = file.read()
print(teststr0)
teststr = copy.deepcopy(teststr0)
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
    works = works and results[0] == emini
    if not works:
        print(results[0])
print(works)


