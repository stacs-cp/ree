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
sys.path.append('../ree/tools')
import subprocess
import EFormatGraph as EFG
import eminipyparser as ep
import os
import gp2Interface
import pandas as pd
import time

def SolveAndTransform() -> int:

## Create Reformulation Graph (node: spec, edge:transform)
## Actions: generate spec, generate instance, transform spec, solve instance
    # event: type, time, space,details
    # events: generate instance (abstract spec to constrete spec), translate (Format to format), transform ( spec to spec), solve (concrete spec to solution)
    # 
    
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
    params = ""
    conjureCall = ['conjure','solve', specFilename]
    subprocess.run(conjureCall, check=True)
    solveTime =time.time_ns() - start


    # TODO upgrade to log solution. time, size, number of nodes traversed
    with open("./conjure-output/model000001-solution000001.solution") as solution:
        s = solution.read()
        parentSolutionID = hash(s)
        print(s)

    formatsGraph = EFG.EFGraph()

    start2 = time.time_ns()
    # Translate to GP2 (could be done in parallel)
    gp2spec = formatsGraph.FormToForm(spec,"Emini","GP2String")
    gp2hostfile = "./gp2/testExpression.host"
    with open(gp2hostfile, 'w') as file:
        file.write(gp2spec)

    # Apply Transform
    progName = "DeMorganTwo.gp2"
    hostGraph = os.path.join("gp2","testExpression.host")
    gp2Interface.runPrecompiledProg(progName,hostGraph)

    gp2specNEW = ""
    transformTime = time.time_ns() - start2
    # If trasform is applicable solve new spec
    if os.path.isfile("gp2.output"):
        with open("gp2.output") as newGP2spec:
            gp2specNEW = newGP2spec.read()
        print(gp2specNEW)
        spec2 = formatsGraph.FormToForm(gp2specNEW,"GP2String","Emini")
        instanceID = hash(spec2)
        print(spec2)
        spec2Filename = "./tests/testExpression2.essence"
        with open(spec2Filename, 'w') as file:
            file.write(spec2)
        start3 = time.time_ns()
        # call conjure and solve spec
        conjureCall2 = ['conjure','solve', spec2Filename]
        subprocess.run(conjureCall2, check=True)

        # TODO upgrade to log solution
        with open("./conjure-output/model000001-solution000001.solution") as solution:
            s = solution.read()
            solutionID = hash(s)
            print(s)
        instanceSolveTime = time.time_ns() - start3
        # Clear files
        os.remove("gp2.output")
        if os.path.isfile("gp2.log"):
            os.remove("gp2.log")
    else:
        # TODO add log
        print("Transform not applied")
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
    for i in range(20):
        data_rows.append(SolveAndTransform())
    print(data_rows)
    dataLogger = pd.DataFrame(data_rows,columns = columns)
    dataLogger.to_csv("experiments/crankSanityCheck.csv")
    sys.exit()
    