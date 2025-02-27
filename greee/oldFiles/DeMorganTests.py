import os
import sys
sys.path.append('greee')
sys.path.append('.')
sys.path.append('../..')
sys.path.append('..')
#import greee
from greee import gp2Interface
import subprocess
from greee import EFormatConverters
from greee import eminipyparser
spec = r'''
find a : bool
find b : bool
find c : bool
such that
    a = !(b /\ c)'''

spec2 = r'''
find a : int(0..20)
such that
    a = 3 * 3'''

specFilename = "./tests/deMorgTest.essence"
with open(specFilename, 'w') as file:
    file.write(spec)

params = ""
conjureCall = ['conjure','solve', specFilename]
subprocess.run(conjureCall, check=True)
AST = EFormatConverters.EminiToASTpy(spec)
eminipyparser.printTree(AST)
with open("./conjure-output/model000001-solution000001.solution") as solution:
    print(solution.read())
new_spec = gp2Interface.transformSpec_u("DeMorganTwo.gp2", spec)

print(new_spec)
specFilename = "./tests/deMorgTestOutput.essence"
with open(specFilename, 'w') as file:
    file.write(new_spec)

params = ""
conjureCall = ['conjure','solve', specFilename]
subprocess.run(conjureCall, check=True)

with open("./conjure-output/model000001-solution000001.solution") as solution:
    print(solution.read())

#os.remove("gp2.output")
