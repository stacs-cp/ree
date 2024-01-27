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

abspec = r'''given i : int(0..100)
where
    i = 1 * 2 + 3 * 4
given a : bool
given b : bool
given c : bool
where
    a = !(b /\ c)'''

spec = etransform_graph.Abstract_to_InstaGen(abspec)
print(spec)

# test spec update to generator call
start = time.time_ns() 


spec_ID = etransform_graph.add_e_node(spec)
solution = etransform_graph.solve(spec_ID)
solveTime =time.time_ns() - start
parentSolutionID = hash(solution)

