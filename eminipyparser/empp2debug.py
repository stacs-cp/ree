import eminipyparser2 as ep
import os
from datetime import datetime
import matplotlib.pyplot as plt
import networkx as nx
input_str = """

letting mytuple be (7)
letting vertices be domain int(1..10)
letting colours be domain int(1..3)
letting G be relation((1,2),(1,3),(2,3),(4,5),(5,6),(6,7),(7,8),(7,9),(8,9),(9,10),(3,4),(6,1),(2,6),(6,3),(10,8),(1,8))
find C : relation of (colours)
such that
  forAll (u,v) in G .
     C(u) != C(v)




"""

parser = ep.EssenceParser()
statements = parser.parse(input_str)
rootTree = ep.Node("GraphColouring", statements)
ep.printTree(rootTree, printInfo=True)

G = ep.getNXTree("GraphColouring", statements)
labels = nx.get_node_attributes(G, 'value')
plt.figure(figsize=(20,20),dpi=40) 
#pos = graphviz_layout(G, prog="dot")
pos = nx.spring_layout(G,k= 3,iterations=450)
#nx.draw(G,pos,with_labels=True,labels=labels, node_size=300, node_color="lightblue", font_size=14, font_weight="bold")
#plt.show()