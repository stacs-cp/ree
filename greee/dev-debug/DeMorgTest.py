import os
import sys
sys.path.append('.')

from greee import EFormatGraph
spec = r'''
given a : bool
given b : int(1..10)
letting c be 5
find d : bool
    such that
        a = (!d \/ !(b>c))'''

ETG = EFormatGraph.EFGraph()
gp2 = ETG.FormToForm(spec,"Emini","GP2String")

hostFileName = "gp2/demorgTest.host"
#with open(hostFileName, 'w') as file:
    #file.write(gp2)
print(gp2)