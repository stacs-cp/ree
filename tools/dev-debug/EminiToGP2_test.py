import sys
sys.path.append('../ree/tools')
import EFormatConverters as ET
import EFormatGraph
import os
import icing
import GP2Interface
from datetime import datetime
import subprocess


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
new_specGP2 = ""
with open(output, 'r') as file:
    new_specGP2 = file.read()

new_spec = EFG.FormToForm(new_specGP2, "GP2String", "Emini")
print(new_spec)

if os.path.exists(output):
  os.remove(output)
  os.remove("gp2.log")

specFilename = "./tests/deMorgTestOutput.essence"
with open(specFilename, 'w') as file:
    file.write(new_spec)

params = ""
conjureCall = ['conjure','solve', specFilename]
subprocess.run(conjureCall, check=True)

with open("./conjure-output/model000001-solution000001.solution") as solution:
    print(solution.read())