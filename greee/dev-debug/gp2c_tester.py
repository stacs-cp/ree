import os
import sys
sys.path.append('greee')
import subprocess
import EFormatGraph

formatsGraph = EFormatGraph.EFGraph()

spec = r'''
such that x = 3 *2
'''
gp2spec = formatsGraph.FormToForm(spec,"Emini","GP2String")
print(gp2spec)



gp2spec2 = '''
[
(0, "*~BinaryExpression")
(1, "operanduno")
(2, "operanddue")
(3, "=~BinaryExpression")
(4, "prexep")
|
(0,0,1,1)
(1,0,2,2)
(2,3,0,1)
(3,3,4,1)
]
'''
gp2spec3 = '''
[
(0,"=~BinaryExpression")
(1,"x~Literal")
(2,"*~BinaryExpression")
(3,"2~Integer")
(4,"4~Integer")
| 
(0,0,1,1)
(1,0,2,2)
(2,2,3,1)
(3,2,4,2)
]'''

gp2hostfile = "gp2/gp2Test.host"
with open(gp2hostfile, 'w') as file:
    file.write(gp2spec3)

gp2prog =  os.path.join("gp2", "stringTest.gp2")

gp2cCall = ["gp2c",gp2prog, gp2hostfile]
subprocess.run(gp2cCall, check=True)