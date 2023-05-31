import sys
sys.path.append('../ree/eminipyparser')
import ETransformulator as ET
import ETTouring
import os
import icing
from datetime import datetime

teststr = """
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
such that
t[1] = t[2]
"""

ast = ET.EminiToASTpy(teststr)
ET.ep.printTree(ast, printInfo=True)
ETG = ETTouring.ETGraph()
GP2 = ETG.FormToForm(teststr,"Emini","GP2String")
print(GP2)

astpy = ETG.FormToForm(GP2,"GP2String","ASTpy")
ET.ep.printTree(astpy, printInfo=True)
Emin = ET.ASTpyToEmini(astpy)
print(Emin)
originalForm = ETG.FormToForm(GP2,"GP2String","Emini")
print(originalForm)


