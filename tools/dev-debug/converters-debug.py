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

nxgraph = ET.ASTpyToNX(ast)

gp2g = ET.NXToGP2Graph(nxgraph)

gp2str = ET.GP2GraphToGP2String(gp2g)

gp2g = ET.GP2StringToGP2Graph(gp2str)

nxgraph = ET.GP2GraphToNX(gp2g)

ast2 = ET.NXToASTpy(nxgraph)

emini3 = ET.ASTpyToEmini(ast2)
print(emini3)
#works = True
#for i in range(0,2):
#    print("TOUR Starts")
#    results = ETG.heuristicChinesePostman(emini2,"Emini")
#    print(results)
#    works = works and results[0] == emini
#    if not works:
#        print(results[0])
#print(works)

