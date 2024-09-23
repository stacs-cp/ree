'''
Baseline experiment 1

- Start experiment logger
    - Generate Instance?
    - Solve Instance
    - Store performance/result
    - Essence to GP2
    - Select Transform Sequence
    - Apply transforms (check if transform rule is applied)
    - Store old-new spec pair as edge
    - GP2 to Essence
    - Check equality or diff
    - Solve new Instance
    - Save to LOGS
'''

import sys
sys.path.append('.')
import pandas as pd
import time
import networkx as nx
import matplotlib.pyplot as plt

from greee import essence_transforms

def SolveAndTransform() -> int:

## Create Reformulation Graph (node: spec, edge:transform)
## Actions: generate spec, generate instance, transform spec, solve instance
    # event: type, time, space,details
    # events: generate instance (abstract spec to constrete spec), translate (Format to format), transform ( spec to spec), solve (concrete spec to solution)
    # 
    etransform_graph = essence_transforms.EssenceTransforms()
    # test spec update to generator call
    start = time.time_ns() 

    spec = r'''find i : int(0..100)
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

    # Transform with GP2 (could be done in parallel)
    progName = "DeMorganTwo.gp2"

    spec2_ID= etransform_graph.transform_with_GP2_and_record(spec_ID,progName)
    transformTime = time.time_ns() - start2
    
    # Solve new spec
    solution2 = etransform_graph.solve(spec2_ID)
    instanceSolveTime = time.time_ns() - transformTime
    solutionID = hash(solution2)


    # PLOT
    pos = nx.spring_layout(etransform_graph.graph)
    nx.draw(etransform_graph.graph, pos)
    node_labels = nx.get_node_attributes(etransform_graph.graph,'file_name')
    nx.draw_networkx_labels(etransform_graph.graph, pos, node_labels)
    edge_labels = dict([((n1, n2), d['transformation']) for n1, n2, d in etransform_graph.graph.edges(data=True)])
    nx.draw_networkx_edge_labels(etransform_graph.graph, pos, edge_labels=edge_labels)
    plt.show(block=True)


    return {'parentID': spec_ID, 
                'childID': spec2_ID, 
                'trasform': progName, 
                'transformTime':transformTime, 
                'parentSolveTime' : solveTime,
                'instanceSolveTime':  instanceSolveTime,
                'parentSolutionID':parentSolutionID, 
                'solutionID':solutionID }
    

    
if __name__ == '__main__':
    # define columns
    columns = ['parentID', 'childID', 'trasform', 'transformTime', 'parentSolveTime', 'instanceSolveTime','parentSolutionID', 'solutionID']  
    data_rows = []
    for i in range(1):
        data_rows.append(SolveAndTransform())
    print(data_rows)
    dataLogger = pd.DataFrame(data_rows,columns = columns)
    #dataLogger.to_csv("experiments/crankSanityCheck.csv")
    sys.exit()
    
