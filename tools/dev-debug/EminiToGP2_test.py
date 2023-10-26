import sys
sys.path.append('../ree/tools')
import EFormatConverters as ET
import EFormatGraph
import os
import icing
import GP2Interface
from datetime import datetime


teststr = r'''
find a : bool
find b : bool
find c : bool
such that
    a = !(b /\ c)'''
EFG = EFormatGraph.ETGraph()
gp2str = EFG.FormToForm(teststr, "Emini","GP2String")
hostFileName = "gp2/demorgTest.host"
with open(hostFileName, 'w') as file:
    file.write(gp2str)

GP2Interface.runPrecompiledProg("DeMorganTwo.gp2",hostFileName)
output = "gp2.output"
with open(output, 'r') as file:
    print(file.read())

if os.path.exists(output):
  os.remove(output)
  os.remove("gp2.log")