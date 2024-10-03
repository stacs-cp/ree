import os
import sys
sys.path.append('.')
import greee.gp2Interface as gp2Interface
import subprocess

spec = r'''
letting a be 1
letting b be 9
letting c be 11
letting d be 100
find Y : int(0..100)
such that
c > Y /\
Y < d /\ 
Y > a /\
b < Y'''

specFilename = "./tests/testExpression.essence"
with open(specFilename, 'w') as file:
    file.write(spec)

params = ""
conjureCall = ['conjure','solve', specFilename]
subprocess.run(conjureCall, check=True)

with open("./conjure-output/model000001-solution000001.solution") as solution:
    print(solution.read())
new_spec = gp2Interface.transformSpec_u("InequalityFlip.gp2", spec)

print(new_spec)
specFilename = "./tests/testExpression.essence"
with open(specFilename, 'w') as file:
    file.write(new_spec)

params = ""
conjureCall = ['conjure','solve', specFilename]
subprocess.run(conjureCall, check=True)

with open("./conjure-output/model000001-solution000001.solution") as solution:
    print(solution.read())

os.remove("gp2.output")
