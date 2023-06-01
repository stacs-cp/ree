import sys
sys.path.append('../ree/tools')
import EFormatConverters as ET
import EFormatGraph
import os
import icing
from datetime import datetime
import copy

teststr0 = """
letting vertices be domain int(1..3)
letting colours be domain int(1..3)
letting G be relation((1,2),(1,3),(2,3))
letting map be domain relation of (vertices * colours)
letting T be domain tuple (vertices,colours)
find C : map
find t : T
such that
forAll (u,c) in C .
    forAll (v,d) in C .
        ((u = v) -> (c = d))
such that
forAll u : vertices .
    exists c : colours . C(u,c)
such that
forAll (u,v) in G .
forAll c,d : colours . (C(u,c) /\ C(v,d) -> (c != d))
such that
t in C
such that t[1] = t[2]
"""

teststr = copy.deepcopy(teststr0)
ast = ET.EminiToASTpy(teststr)
#ET.ep.printTree(ast, printInfo=True)

emini = ET.ASTpyToEmini(ast)
ETG = EFormatGraph.ETGraph()

emini2 = copy.deepcopy(teststr)
works = True
for i in range(0,100):
    results = ETG.heuristicChinesePostman(emini2,"Emini")
    works = works and results[0] == emini
print(works)


