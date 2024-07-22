import sys
sys.path.append('.')

from greee import EFormatGraph
from greee import essence2rules_tools
import networkx as nx
import matplotlib.pyplot as plt

gcmulti = r"""


find x :int(0..100)
such that
 x <= 5*2
"""
EFG = EFormatGraph.EFGraph()
gp2g = EFG.FormToForm(gcmulti, "Emini","GP2Graph")
gp2_partial_rule = essence2rules_tools.GP2GraphToGP2StringB_rule_precursor(gp2g)
print("______Partial Rule____\n" ,gp2_partial_rule)

preserved_nodes= [0,1,2,3,4,5]
gp2_partial_rule2 = essence2rules_tools.GP2GraphToGP2StringB_rule_precursor(gp2g,preserved_nodes)
print("______Partial Rule Chopped____\n", gp2_partial_rule2)
nxLeftover = EFG.FormToForm(gp2_partial_rule2,"GP2StringB", "NX")
print("____", len(nxLeftover.nodes))
nx.draw(nxLeftover, with_labels = True)
plt.show()
eministr = EFG.FormToForm(gp2_partial_rule2, "GP2StringB","Emini")
print("______New Essence____\n",eministr)

