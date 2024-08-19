import sys
sys.path.append('.')

from greee import EFormatGraph
from greee import essence2rules_tools
import networkx as nx
import matplotlib.pyplot as plt
from deepdiff import DeepDiff, Delta
import pprint

gcmulti = r"""
find x :int(0..100)
such that
 x <= 5*2
"""

EFG = EFormatGraph.EFGraph()
gcmulti = EFG.FormToForm(gcmulti, "Emini","ASTpy")
gcmulti = EFG.FormToForm(gcmulti, "ASTpy", "Emini")
gp2g = EFG.FormToForm(gcmulti, "Emini","GP2Graph")
gp2_partial_rule = essence2rules_tools.GP2GraphToGP2StringB_rule_precursor(gp2g)
print("______Partial Rule____\n" ,gp2_partial_rule)

preserved_nodes= [0,1,2,3,4,5]
gp2_partial_rule2 = essence2rules_tools.GP2GraphToGP2StringB_rule_precursor(gp2g,preserved_nodes)
print("______Partial Rule Chopped____\n", gp2_partial_rule2)
nxLeftover = EFG.FormToForm(gp2_partial_rule2,"GP2StringB", "NX")
#print("____", len(nxLeftover.nodes))
#nx.draw(nxLeftover, with_labels = True)

eministr = EFG.FormToForm(gp2_partial_rule2, "GP2StringB","Emini")
print("______New Essence____\n",eministr)

preserved_nodes= [0,1,2,3,4,5]
param_nodes = []
gp2_partial_rule2 = essence2rules_tools.GP2GraphToGP2StringB_rule_precursor(gp2g,preserved_nodes,param_nodes)
print("______Partial Parametrised Rule____\n", gp2_partial_rule2)
nxLeftoverAST = EFG.FormToForm(gp2_partial_rule2,"GP2StringB", "ASTpy")
nxLeftoverAST = EFG.FormToForm(nxLeftoverAST,"ASTpy", "Emini")
nxLeftoverAST = EFG.FormToForm(nxLeftoverAST,"Emini","ASTpy")

originalAST = EFG.FormToForm(gcmulti, "Emini","ASTpy")

diff = DeepDiff(originalAST,nxLeftoverAST)
print("OBJECT DIFF: \n:", diff)
delta = Delta(diff)
print("OBJECT DELTA: \n:", delta)

diff2 = DeepDiff(gcmulti, eministr)

print("STRING DIFF: \n:", diff2)
delta2 = Delta(diff2)
print("STRING DELTA: \n:", delta2)

spec = r'''
$ k-fold graph colouring with k=coloursPerNode, out of numberColours
given n : int(0..100)
letting vertices be domain int(0..n-1)
given edges : relation (irreflexive) of ( vertices * vertices )
given numberColours : int(1..n)
given coloursPerNode : int(1..n)
letting colours be domain int(1..numberColours)
find c : relation (size n*coloursPerNode) of ( vertices * colours )
such that true

$ endpoints of edges do not share colours
,  forAll (u,v) in edges .
      (forAll colourAssignment in c .
         (colourAssignment[1] = u) -> !((v,colourAssignment[2]) in c))

$ enforce number of colours per node
,  forAll u : vertices .
      coloursPerNode = (sum colourAssignment in c .
         toInt(colourAssignment[1] = u))
'''

spec2 = r'''
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
      c(v) intersect c(u) = {}'''

diff2 = DeepDiff(spec, spec2)

print("STRING DIFF: \n:", diff2)
delta2 = Delta(diff2)
print("STRING DELTA: \n:", delta2)

ast1 = EFG.FormToForm(spec, "Emini","GP2Graph")
ast2 = EFG.FormToForm(spec2, "Emini","GP2Graph")

diff = DeepDiff(ast1,ast2)
print("OBJECT DIFF: \n:", diff)
delta = Delta(diff)
print("OBJECT DELTA: \n")
pprint.pprint(delta)

print("_________\n",EFG.FormToForm(ast1, "GP2Graph","GP2StringB"))
preserved_nodes = [13,14,16]
gp2_partial_rule2 = essence2rules_tools.GP2GraphToGP2StringB_rule_precursor(ast1,preserved_nodes,param_nodes)
