import sys
sys.path.append('.')

from greee import EFormatGraph
import networkx as nx
import matplotlib.pyplot as plt

gp2string = r'''[
    (0, "abc":"def":"ghi":"jkl")
    (1, 2:"mnopqrstuvwxyz")
    (2, 1:"one":2:"two")
    (3, 6:6:6:6:6:6:6:6:6:6:6:6:6)
    (4, empty)
|
    (0, 0, 1, 0)
    (1, 0, 1, 0 # red)
    (2, 0, 2, "2" # blue)
    (3, 1, 3, empty # dashed)
    (4, 2, 2, empty # green)
    (4, 2, 2, empty)
    (5, 2, 3, empty # red)
    (6, 2, 4, 6:6:6:6:5:6:6)
    (7, 2, 4, 6:6:6:6:5:6:6 # dashed)
] '''

string = gp2string.replace(")","~)")

EFG = EFormatGraph.EFGraph()

g = EFG.FormToForm(string,"GP2String","NX")
labels = nx.get_node_attributes(g, 'label') 
nx.draw(g,labels=labels,with_labels=True)
plt.show(block=True)