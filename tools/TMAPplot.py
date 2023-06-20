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

formsGraph.add_node("Eprime")
EprimePos = cmath.polar(complex(pos["Emini"][0]+0.5,pos["Emini"][1]))
pos["Eprime"] = EprimePos


EprimePos = cmath.polar(complex(pos["Emini"][0]+0.5,pos["Emini"][1]))
pos["Eprime"] = EprimePos
print(EprimePos)
print(pos["Emini"])
nx.draw(formsGraph, pos, with_labels=True, node_size=300, connectionstyle="arc3,rad=-0.1")
plt.show()

