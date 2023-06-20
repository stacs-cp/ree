import sys
sys.path.append('../ree/tools')
import EFormatConverters as ET
import EFormatGraph
import os
import icing
from datetime import datetime
import copy

teststr0 = '''
letting n be 12
letting vertices be domain int(0..n)
find edges : relation (size n) of (vertices * vertices)
such that
      forAll edge,edge2 in edges .
        edge[2] > edge[1] /\ 
        ((edge != edge2) -> (edge[2] != edge2[2]))
'''

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


