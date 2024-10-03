import sys
sys.path.append('.')
from greee import EFormatConverters as EFC
from greee import EFormatGraph



teststr = r'''
find a : bool
such that
a = !(b /\ c)'''
EFG = EFormatGraph.EFGraph()
gp2str = EFG.FormToForm(teststr, "Emini","GP2StringDT")
print(gp2str)