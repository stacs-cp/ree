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
import GP2Interface



def SolveAndTransform() -> int:

## Create Reformulation Graph (node: spec, edge:transform)
## Actions: generate spec, generate instance, transform spec, solve instance
    
    # test spec update to generator call
    spec = '''
    find i : int(0..100)
    such that
        i = 1 * 2 + 3 * 4
    find a : bool
    find b : bool
    find c : bool
    such that
        a = !(b /\ c)'''

    # save spec to file. store file size + time
    specFilename = "./tests/testExpression.essence"
    with open(specFilename, 'w') as file:
        file.write(spec)

    # call conjure and solve spec.
    params = ""
    conjureCall = ['conjure','solve', specFilename]
    subprocess.run(conjureCall, check=True)

    # TODO upgrade to log solution. time, size, number of nodes traversed
    with open("./conjure-output/model000001-solution000001.solution") as solution:
        print(solution.read())

    formatsGraph = EFG.ETGraph()

    # Translate to GP2 (could be done in parallel)
    gp2spec = formatsGraph.FormToForm(spec,"Emini","GP2String")
    gp2hostfile = "./gp2/testExpression.host"
    with open(gp2hostfile, 'w') as file:
        file.write(gp2spec)

    # Apply Transform
    progName = "DeMorganTwo.gp2"
    hostGraph = os.path.join("gp2","testExpression.host")
    GP2Interface.runPrecompiledProg(progName,hostGraph)

    gp2specNEW = ""
    
    # If trasform is applicable solve new spec
    if os.path.isfile("gp2.output"):
        with open("gp2.output") as newGP2spec:
            gp2specNEW = newGP2spec.read()
        print(gp2specNEW)
        spec2 = formatsGraph.FormToForm(gp2specNEW,"GP2String","Emini")
        print(spec2)
        spec2Filename = "./tests/testExpression2.essence"
        with open(spec2Filename, 'w') as file:
            file.write(spec2)

        # call conjure and solve spec
        conjureCall2 = ['conjure','solve', spec2Filename]
        subprocess.run(conjureCall2, check=True)

        # TODO upgrade to log solution
        with open("./conjure-output/model000001-solution000001.solution") as solution:
            print(solution.read())
        
        # Clear files
        os.remove("gp2.output")
        if os.path.isfile("gp2.log"):
            os.remove("gp2.log")
    else:
        # TODO add log
        print("Transform not applied")

    
if __name__ == '__main__':
    sys.exit(SolveAndTransform())
    