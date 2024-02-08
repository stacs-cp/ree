import sys
sys.path.append('.')
import subprocess
import os
import pandas as pd
import time
import matplotlib.pyplot as plt
from greee import essence_transforms
import networkx as nx


et = essence_transforms.EssenceTransforms()

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

spec_ID = et.add_e_node(spec,"StartSpec.essence")
print(et.determine_node_role(spec_ID))
print(et.instace_specs_list)
#solution = etransform_graph.solve(spec_ID)
#solveTime =time.time_ns() - start
#parentSolutionID = hash(solution)

print("MAB")
for _ in range(0,20):
    et.expand_from_node(spec_ID)
print(et.instace_specs_list)

 # PLOT
pos = nx.spring_layout(et.graph)
nx.draw(et.graph, pos)
node_labels = nx.get_node_attributes(et.graph,'file_name')
nx.draw_networkx_labels(et.graph, pos, node_labels)
edge_labels = dict([((n1, n2), d['transformation']) for n1, n2, d in et.graph.edges(data=True)])
nx.draw_networkx_edge_labels(et.graph, pos, edge_labels=edge_labels)
plt.show(block=True)

nx.write_gexf(et.graph, "transformtest.gexf")
