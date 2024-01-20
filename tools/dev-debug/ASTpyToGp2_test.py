import sys
sys.path.append('../ree/tools')
import EFormatConverters as EFC
import EFormatGraph
import os
import icing
from datetime import datetime


teststr = r"""
find x : int(0..100)
such that
    1*(2+3)*4 = x /\ (true \/ false)
"""

ast = EFC.EminiToASTpy(teststr)
EFC.ep.printTree(ast, printInfo=True)
ETG = EFormatGraph.EFGraph()
GP2 = ETG.FormToForm(teststr,"Emini","GP2String")
print(GP2)

astpy = ETG.FormToForm(GP2,"GP2String","ASTpy")
EFC.ep.printTree(astpy, printInfo=True)
Emin = EFC.ASTpyToEmini(astpy)
print(Emin)
originalForm = ETG.FormToForm(GP2,"GP2String","Emini")
print(originalForm)


