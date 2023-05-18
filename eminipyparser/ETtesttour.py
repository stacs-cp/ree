import ETransformulator as ET
import GP2Graph
import networkx as nx
from inspect import signature
import matplotlib.pyplot as plt

#forms = ["EminiSpec","ASTpy","1DTokens","ASTNX","ASTpyJson","GP2Graph","Neo4j"]

formsGraph = nx.DiGraph()

for val in ET.__dict__.values():
  if(callable(val)):
    fromTo = val.__name__.split('To')
    formsGraph.add_edge(fromTo[0],fromTo[1], func = val.__name__)

    #val("find i : int(0..3)")

##print(formsGraph.edges(data=True))
plt.figure(figsize=(8,8),dpi=80)

nx.draw_circular(formsGraph,with_labels=True, node_size=300)
plt.show()