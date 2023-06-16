# place holder for full test including conjure and GP2 prog
import sys
sys.path.append('../ree/tools')
import subprocess
import EFormatGraph
import os

spec = '''
find i : int(0..100)
such that
i = 1 * 2 + 3 * 4'''

specFilename = "./tests/testExpression.essence"
with open(specFilename, 'w') as file:
    file.write(spec)

params = ""
conjureCall = ['conjure','solve', specFilename]
subprocess.run(conjureCall, check=True)

with open("./conjure-output/model000001-solution000001.solution") as solution:
    print(solution.read())

formatsGraph = EFormatGraph.ETGraph()

gp2spec = formatsGraph.FormToForm(spec,"Emini","GP2String")
gp2hostfile = "./gp2/testExpression.host"
with open(gp2hostfile, 'w') as file:
    file.write(gp2spec)

gp2prog = "./gp2/commuteMul.gp2"

gp2cCall = ["gp2c",gp2prog, gp2hostfile]
subprocess.run(gp2cCall, check=True)

gp2specNEW = ""
with open("gp2.output") as newGP2spec:
    gp2specNEW = newGP2spec.read()

spec2 = formatsGraph.FormToForm(gp2specNEW,"GP2String","Emini")
print(spec2)
spec2Filename = "./tests/testExpression2.essence"
with open(spec2Filename, 'w') as file:
    file.write(spec2)

conjureCall2 = ['conjure','solve', spec2Filename]
subprocess.run(conjureCall2, check=True)

with open("./conjure-output/model000001-solution000001.solution") as solution:
    print(solution.read())

os.remove("gp2.output")