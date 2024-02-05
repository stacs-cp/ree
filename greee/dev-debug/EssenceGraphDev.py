import sys
sys.path.append('.')
import subprocess
import os
import pandas as pd
import time
import matplotlib.pyplot as plt
from greee import et_graph
import networkx as nx


etransform_graph = et_graph.EssenceTransformGraph()

spec = r'''find i : int(0..100)
such that
    i = 1 * 2 + 3 * 4
find a : bool
find b : bool
find c : bool
such that
    a = !(b /\ c)'''
print(spec)

# test spec update to generator call
start = time.time_ns() 
with open("StartSpec.essence", 'w') as file:
    file.write(spec)

spec_ID = etransform_graph.add_e_node(spec,"StartSpec.essence")
#solution = etransform_graph.solve(spec_ID)
#solveTime =time.time_ns() - start
#parentSolutionID = hash(solution)

print("MAB")
for _ in range(0,10):
    etransform_graph.expand_from_node(spec_ID)
print(etransform_graph.graph.nodes(data=True))

 # PLOT
pos = nx.spring_layout(etransform_graph.graph)
nx.draw(etransform_graph.graph, pos)
node_labels = nx.get_node_attributes(etransform_graph.graph,'file_name')
nx.draw_networkx_labels(etransform_graph.graph, pos, node_labels)
edge_labels = dict([((n1, n2), d['transformation']) for n1, n2, d in etransform_graph.graph.edges(data=True)])
nx.draw_networkx_edge_labels(etransform_graph.graph, pos, edge_labels=edge_labels)
plt.show(block=True)

nx.write_gexf(etransform_graph.graph, "transformtest.gexf")
