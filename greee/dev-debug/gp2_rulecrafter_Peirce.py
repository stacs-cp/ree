import sys
sys.path.append('.')

from greee import EFormatGraph
from greee import essence2rules_tools
import networkx as nx
import matplotlib.pyplot as plt

gcmulti = r"""
letting Q be true
find P : bool
such that
 (P -> Q) -> P """
EFG = EFormatGraph.EFGraph()
gp2g = EFG.FormToForm(gcmulti, "Emini","GP2Graph")

preserved_nodes= [8,9,10,11,12]
gp2_partial_rule2 = essence2rules_tools.GP2GraphToGP2StringB_rule_precursor(gp2g,preserved_nodes)
print("______Partial Rule Chopped____\n", gp2_partial_rule2)
