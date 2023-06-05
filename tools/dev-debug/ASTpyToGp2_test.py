import sys
sys.path.append('../ree/tools')
import EFormatConverters as ET
import EFormatGraph
import os
import icing
from datetime import datetime


teststr = """
find i : int(0..10)
such that
    1*(2+3*4)-8887=i
"""

ast = ET.EminiToASTpy(teststr)
ET.ep.printTree(ast, printInfo=True)
ETG = EFormatGraph.ETGraph()
GP2 = ETG.FormToForm(teststr,"Emini","GP2String")
print(GP2)

astpy = ETG.FormToForm(GP2,"GP2String","ASTpy")
ET.ep.printTree(astpy, printInfo=True)
Emin = ET.ASTpyToEmini(astpy)
print(Emin)
originalForm = ETG.FormToForm(GP2,"GP2String","Emini")
print(originalForm)


