#!/usr/bin/env python3
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

def experiment_vis_file() -> int:
    '''
    given a path on stdin, run code from experiment_vis_dev on contents of file
    '''

    import argparse
    p = argparse.ArgumentParser(description="run experiment_vis_dev on files")
    p.add_argument('file', nargs='+', help='Essence spec')
    args = p.parse_args(args=sys.argv[1:])

    from pathlib import Path
    specfile = ''
    for f in args.file:
        specfile = Path(f)
        if not specfile.is_file():
            sys.exit(str(specfile) + ' is not a valid file, quitting')

        with open(specfile, 'r') as infile:
            spec = infile.read()

        et = essence_transforms.EssenceTransforms()

        print(spec)

        # test spec update to generator call
        start = time.time_ns() 
        with open("StartSpec.essence", 'w') as file:
            file.write(spec)

        spec_ID = et.add_e_node(spec,"StartSpec.essence")
        #solution = etransform_graph.solve(spec_ID)
        #solveTime =time.time_ns() - start
        #parentSolutionID = hash(solution)

        for _ in range(0,50):
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
        with open("experiments/transform_solve_test.json", 'w') as file:
                s2 = s.replace("\\n", "<br/>")
                file.write(s2)

if __name__ == '__main__':
    sys.exit(experiment_vis_file())

