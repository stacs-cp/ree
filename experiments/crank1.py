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
sys.path.append('greee')
import subprocess
import os
import gp2Interface
import pandas as pd
import time

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

    spec = '''
    find i : int(0..100)
    such that
        i = 1 * 2 + 3 * 4
    find a : bool
    find b : bool
    find c : bool
    such that
        a = !(b /\ c)'''

    parentID = hash(spec)

    # save spec to file. store file size + time
    specFilename = "./tests/testExpression.essence"
    with open(specFilename, 'w') as file:
        file.write(spec)

    # call conjure and solve spec.
    solution = etransform_graph.solve_from_file(specFilename)
    solveTime =time.time_ns() - start
    parentSolutionID = hash(solution)

    # TODO upgrade logs: solution. time, size, number of nodes traversed
    
    start2 = time.time_ns()

    # Translate to GP2 (could be done in parallel)
    progName = "DeMorganTwo.gp2"
    if not os.path.isdir(os.path.join("gp2","Compiled",progName[-4])):
        gp2Interface.compileGP2Program(progName)
    spec2= etransform_graph.transform_with_GP2_and_record(spec,progName)
    transformTime = time.time_ns() - start2

    instanceID = hash(spec2)
    print(spec2)
    spec2Filename = "./tests/testExpression2.essence"
    with open(spec2Filename, 'w') as file:
        file.write(spec2)
    start3 = time.time_ns()
    solution2 = etransform_graph.solve_from_file(spec2Filename)
    instanceSolveTime = time.time_ns() - start3
    solutionID = hash(solution2)


    return {'instanceID': instanceID, 
                'parentID': parentID, 
                'trasform': progName, 
                'transformTime':transformTime, 
                'parentSolveTime' : solveTime,
                'instanceSolveTime':  instanceSolveTime,
                'parentSolutionID':parentSolutionID, 
                'solutionID':solutionID }
    

    
if __name__ == '__main__':
    # define columns
    columns = ['instanceID', 'parentID', 'trasform', 'transformTime', 'parentSolveTime', 'instanceSolveTime','parentSolutionID', 'solutionID']  
    data_rows = []
    for i in range(5):
        data_rows.append(SolveAndTransform())
    print(data_rows)
    dataLogger = pd.DataFrame(data_rows,columns = columns)
    dataLogger.to_csv("experiments/crankSanityCheck.csv")
    sys.exit()
    