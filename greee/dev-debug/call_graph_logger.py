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
from networkx.readwrite import json_graph

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

    spec = r'''letting a be 3
    letting intDom be domain int(1..3)

    letting fff be function (3-->7,2-->a)
    letting ggg be 44                 
    find f : function (minSize 1*2, maxSize 48/2+a, total) tuple(intDom,intDom) --> set of int(1..90)'''
    print(spec)

    # test spec update to generator call
    start = time.time_ns() 
    with open("StartSpec.essence", 'w') as file:
        file.write(spec)

    spec_ID = et.add_e_node(spec,"StartSpec.essence")
    #solution = etransform_graph.solve(spec_ID)
    #solveTime =time.time_ns() - start
    #parentSolutionID = hash(solution)


    for _ in range(0,30):
        selected_node = et.select_current_node()
        et.expand_from_node(selected_node,solve_spec=True)
    print(et.graph.nodes(data=True))

 # PLOT
#pos = nx.spring_layout(et.graph)
pos = nx.spectral_layout(et.graph)
nx.draw(et.graph, pos)
node_labels = nx.get_node_attributes(et.graph,'file_name')
nx.draw_networkx_labels(et.graph, pos, node_labels)
edge_labels = dict([((n1, n2), d['transformation']) for n1, n2, d in et.graph.edges(data=True)])
nx.draw_networkx_edge_labels(et.graph, pos, edge_labels=edge_labels)
plt.show(block=True)
nx.write_gexf(et.graph, "transform_solve_test.gexf")
data = json_graph.node_link_data(et.graph)
import json
s = json.dumps(data)
with open("transform_solve_test.json", 'w') as file:
        s2 = s.replace("\\n", "<br/>")
        #file.write(s2)