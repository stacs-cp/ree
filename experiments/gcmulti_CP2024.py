import sys
sys.path.append('.')
import subprocess

from greee import instaGen
import networkx as nx
import time
import csv
import os
import signal

fields = ['SpecName', 'nodes','edges','colours','coloursPerNode','NewSpec', 'OldSpec'] 
   
# data rows of csv file 
rows = []
filename = 'ParamSpanResults.csv'
 
with open(filename, 'a') as f:
     
    # using csv.writer method from CSV package
    write = csv.writer(f)
     
    write.writerow(fields)


for i in range(1,5): # 1,5
    for j in range(2,7): #2,7
        for k in range(4,6):
            for l in range(2,5):
                test_string = ""
                nodes = i*10
                edges = int((nodes**2)*j*0.05)
                test_graph = nx.gnm_random_graph(nodes,edges)
                #test_graph = nx.dodecahedral_graph()
                #test_graph = nx.ring_of_cliques(2,5)
                #print(*test_graph.edges(data=False))
                availableColours= min(nodes,k*l)
                test_string += instaGen.NXtoEssenceRelationForGCmulti(test_graph, "n","edges") + " \n"
                test_string += f"letting numberColours be {availableColours} \n"
                test_string += f"letting coloursPerNode be {l} \n"

                #print(test_string)
                graphcolouring_file = f"tests/gcmulti_rand-{nodes}-{edges}-{availableColours}-{l}.param"

                spec = "tests/gcmulti-func.essence"
                specOld = "tests/gcmulti.essence"

                
                with open(graphcolouring_file, 'w') as file:
                    file.write(test_string)

                conjureCall = ['conjure','solve', spec,graphcolouring_file ]
                start = time.time_ns() 
                # Start the subprocess in a new process group
                proc = subprocess.Popen(conjureCall, preexec_fn=os.setsid)

                try:
                    # Wait for the process to complete, or kill it after a timeout
                    proc.wait(timeout=60)
                except subprocess.TimeoutExpired:
                    # Send the signal to all the processes in the process group
                    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                
                solveTime =time.time_ns() - start
                solveTime = round(solveTime/1000000000,2)
                print(solveTime)
                if solveTime > 59:
                    solveTime = "TO"


                

                with open(graphcolouring_file, 'w') as file:
                    file.write(test_string)

                conjureCall = ['conjure','solve', specOld,graphcolouring_file ]
                start2 = time.time_ns() 
                
                proc = subprocess.Popen(conjureCall, preexec_fn=os.setsid)

                try:
                    # Wait for the process to complete, or kill it after a timeout
                    proc.wait(timeout=60)
                except subprocess.TimeoutExpired:
                    # Send the signal to all the processes in the process group
                    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)

                solveTime2 =time.time_ns() - start2
                solveTime2 = round(solveTime2/1000000000,2)
                print(solveTime2)
                if solveTime2 > 59:
                    solveTime2 = "TO"
                with open(filename, 'a') as f:
     
                    # using csv.writer method from CSV package
                    write = csv.writer(f)
                    
                    write.writerow([graphcolouring_file,nodes,edges,availableColours,l,solveTime,solveTime2])

                

