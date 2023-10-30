import sys
sys.path.append('../ree/tools')
import EFormatConverters as ET
import EFormatGraph
import os
import icing
from datetime import datetime
import copy

teststr0 = r'''
find b : bool such that b = exists i : int(0..4) . i*i=i
'''
teststr2 = r'''
letting a be domain int(0..10)
find b : int(0..100)
find c : int(0..100)
letting G be relation((1,2),(1,3),(2,3))

such that
 b = sum i : a .1
such that
 c = forAll v in G . v[1] *2
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


