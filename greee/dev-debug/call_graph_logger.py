from pycallgraph2 import PyCallGraph
from pycallgraph2.output import GraphvizOutput
from pycallgraph2 import GlobbingFilter
from pycallgraph2 import Config


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
config = Config()


trace_filter = GlobbingFilter(exclude=[
    'pycallgraph.*',
    're.*',
    'contextlib.*',
    'itemsview.*',
    'subprocess.Popen._*',
    '__*'
])
config.trace_filter = trace_filter



with PyCallGraph(config=config,output=graphviz):


    graphviz.output_file = 'output.svg'
    graphviz.output_type = 'svg'
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
    #solution = etransform_graph.solve(spec_ID)
    #solveTime =time.time_ns() - start
    #parentSolutionID = hash(solution)


    for _ in range(0,100):
        selected_node = et.select_current_node()
        et.expand_from_node(selected_node)
    print(et.graph.nodes(data=True))

