from pycallgraph2 import PyCallGraph
from pycallgraph2.output import GraphvizOutput

import sys
sys.path.append('.')
import subprocess
import os
import pandas as pd
import time
import matplotlib.pyplot as plt
from greee import essence_transforms
import networkx as nx
graphviz = GraphvizOutput()

with PyCallGraph(graphviz):
    graphviz.output_file = 'output.svg'
    graphviz.output_type = 'svg'
    etransform_graph = essence_transforms.EssenceTransforms()

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
    for _ in range(0,5):
        etransform_graph.expand_from_node(spec_ID)
    print(etransform_graph.graph.nodes(data=True))

