import sys
sys.path.append('.')

from greee import EFormatGraph



gcmulti = r'''

given n : int(0..100)
letting vertices be domain int(0..n-1)
given edges : relation (irreflexive) of ( vertices * vertices )
given numberColours : int(1..n)
given coloursPerNode : int(1..n)
letting colours be domain int(1..numberColours)
letting coloursSet be domain set (size coloursPerNode) of colours
find c : function (total) vertices --> coloursSet
such that
forAll (u,v) in edges .
      c(v) intersect c(u) = {}
'''

gcmulti = r"""


find x :int(0..100)
such that
 x <= 5*2
"""
EFG = EFormatGraph.EFGraph()
gp2str = EFG.FormToForm(gcmulti, "Emini","GP2StringDT")
hostFileName = "gp2/gcmultifunc_DT.host"
with open(hostFileName, 'w') as file:
    file.write(gp2str)

print(gp2str)
spec_nx = EFG.FormToForm(gp2str, "GP2StringDT","NX")

Eministr = EFG.FormToForm(spec_nx, "NX","Emini")
print(Eministr)

