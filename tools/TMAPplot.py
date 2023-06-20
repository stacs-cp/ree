import EFormatConverters as ET
import GP2Graph
import networkx as nx
from inspect import signature
import matplotlib.pyplot as plt
import cmath
import math
#forms = ["EminiSpec","ASTpy","1DTokens","ASTNX","ASTpyJson","GP2Graph","Neo4j"]


 
formsGraph = nx.DiGraph()

for val in ET.__dict__.values():
    if(callable(val)):
        fromTo = val.__name__.split('To')
        formsGraph.add_edge(fromTo[0],fromTo[1], func = val.__name__)

plt.figure(figsize=(8,8),dpi=80)

pos = nx.circular_layout(formsGraph)
print(pos)

#nx.draw_circular(formsGraph,with_labels=True, node_size=300, connectionstyle="arc3,rad=-0.1" )
#plt.savefig("formsMap.png")
for p  in pos.values():
    z = complex(p[0],p[1])
    z= cmath.polar(z)
    #print(z)

def polarToCartesian(radius, phi):
    theta = phi * math.pi/180.0;
    x = radius * math.cos(theta)
    y = radius * math.sin(theta)
    return [x,y]

def polar(x, y):
    """returns r, theta(degrees)
    """
    r = (x ** 2 + y ** 2) ** .5
    theta = math.degrees(math.atan2(y,x))
    return [r, theta]

tempos = pos["Emini"]
pos["Emini"] = pos["Json"] 
pos["Json"] = tempos

srd = 0.6 # Second ring distance

formsGraph.add_node("Eprime")
formsGraph.add_edge("Emini", "Eprime")
polarPos = polar(pos["Emini"][0],pos["Emini"][1])
EprimePos = polarToCartesian(polarPos[0]+srd,polarPos[1])
pos["Eprime"] = EprimePos

SavileRowOutputs = ["MiniZinc","FlatZinc","Minion","Gecode","SMT", "MaxSAT", "SAT"]

separation = 9;
for i,output in enumerate(SavileRowOutputs):
    formsGraph.add_node(output)
    formsGraph.add_edge("Eprime",output)
    
    outputPos = polar(pos["Emini"][0],pos["Emini"][1])
    outputPos = polarToCartesian(outputPos[0]+srd+0.5, outputPos[1]-(len(SavileRowOutputs)*separation)/2+(i*separation))
    pos[output] = outputPos

formsGraph.add_node("GP2")
formsGraph.add_edge("GP2String", "GP2")
polarPos = polar(pos["GP2String"][0],pos["GP2String"][1])
GP2Pos = polarToCartesian(polarPos[0]+srd, polarPos[1])
pos["GP2"] = GP2Pos

formsGraph.add_node("ML")
formsGraph.add_edge("NX", "ML")
polarPos = polar(pos["NX"][0],pos["NX"][1])
GNNPos = polarToCartesian(polarPos[0]+srd, polarPos[1])
pos["ML"] = GNNPos

formsGraph.add_node("Comms")
formsGraph.add_edge("Json", "Comms")
polarPos = polar(pos["Json"][0],pos["Json"][1])
CommsPos = polarToCartesian(polarPos[0]+srd, polarPos[1])
pos["Comms"] = CommsPos

print(pos)
print(pos["Emini"])

figure, axes = plt.subplots(figsize=(9,9))

Drawing_uncolored_circle = plt.Circle( (0.0, 0.0 ),
                                      1.0 ,
                                      alpha=0.1,
                                      color='#33ffff',
                                      )

axes.add_artist( Drawing_uncolored_circle )
axes.set_aspect('equal')

figure.tight_layout()

nx.draw(formsGraph, pos, with_labels=True, node_size=1400, connectionstyle="arc3,rad=-0.1")
plt.show()

