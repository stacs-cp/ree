import sys
sys.path.append('greee')
import subprocess
import os
import gp2Interface
import pandas as pd
import time
import matplotlib.pyplot as plt
import et_graph
import networkx as nx


etransform_graph = et_graph.EssenceTransformGraph()
# test spec update to generator call
start = time.time_ns() 

spec = '''find i : int(0..100)
such that
i = 1 * 2 + 3 * 4
find a : bool
find b : bool
find c : bool
such that
a = !(b /\ c)'''

spec_ID = etransform_graph.add_e_node(spec)
solution = etransform_graph.solve(spec_ID)
solveTime =time.time_ns() - start
parentSolutionID = hash(solution)

# TODO upgrade logs: solution. time, size, number of nodes traversed

start2 = time.time_ns()

# Translate to GP2 (could be done in parallel)
progName = "DeMorganTwo.gp2"

if not os.path.isdir(os.path.join("gp2","Compiled",progName[-4])):
    gp2Interface.compileGP2Program(progName)
spec2= etransform_graph.transform_with_GP2(spec,progName)
transformTime = time.time_ns() - start2



spec2ID = etransform_graph.add_e_node(spec2)
print(spec2)
etransform_graph.add_e_edge(spec_ID,spec2ID,progName)
spec2Filename = "./tests/testExpression2.essence"
with open(spec2Filename, 'w') as file:
    file.write(spec2)
start3 = time.time_ns()
solution2 = etransform_graph.solve_from_file(spec2Filename)
instanceSolveTime = time.time_ns() - start3
solutionID = hash(solution2)

pos = nx.spring_layout(etransform_graph.graph)

nx.draw(etransform_graph.graph, pos,with_labels=True)
node_labels = nx.get_node_attributes(etransform_graph.graph,'file_name')
nx.draw_networkx_labels(etransform_graph.graph, pos, node_labels)
edge_labels = nx.get_edge_attributes(etransform_graph.graph,"transformation_name")
print("labels")
print(edge_labels)
nx.draw_networkx_edge_labels(etransform_graph.graph, pos, edge_labels=edge_labels)
plt.show(block=True)
plt.savefig("testgraph.png", format="PNG")