import sys
sys.path.append('.')

from greee import EFormatGraph



gcmulti = r'''

letting G be relation((1,2),(1,3),(2,3))
find x :int(0..100)

such that
 x <= (5+4)+(2+1)
such that
  forAll (u,c) in G . 3
such that
5=5
find b : bool such that b = exists i : int(0..4) . i*i=i
'''
EFG = EFormatGraph.EFGraph()
gp2str = EFG.FormToForm(gcmulti, "Emini","GP2StringDT")
hostFileName = "gp2/DT_test.host"
with open(hostFileName, 'w') as file:
    file.write(gp2str)

print(gp2str)
spec_nx = EFG.FormToForm(gp2str, "GP2StringDT","NX")

Eministr = EFG.FormToForm(spec_nx, "NX","Emini")
print(Eministr)

