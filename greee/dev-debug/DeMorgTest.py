import os
import sys
sys.path.append('greee')
import subprocess
import EFormatConverters
import eminipyparser
import EFormatGraph
spec = r'''
find a : bool
find b : bool
find c : bool
such that
    a = !(b /\ c)'''

ETG = EFormatGraph.EFGraph()
gp2 = ETG.FormToForm(spec,"Emini","GP2String")

hostFileName = "gp2/demorgTest.host"
with open(hostFileName, 'w') as file:
    file.write(gp2)