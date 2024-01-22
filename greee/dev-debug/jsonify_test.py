import sys
sys.path.append('greee')
import eminipyparser as ep
from typing import List
import json
import networkx as nx
from networkx.readwrite import json_graph


#test 4
test_strings = """
letting vertices be domain int(1..3)
letting colours be domain int(1..3)
letting G be relation((1,2),(1,3),(2,3))
letting map be domain relation of (vertices * colours)
letting T be domain tuple (vertices,colours)
find C : map
find t : T
such that
  forAll (u,c) in C .
     forAll (v,d) in C .
        ((u = v) -> (c = d))
such that
  forAll u : vertices .
     exists c : colours . C(u,c)
such that
  forAll (u,v) in G .
     forAll c,d : colours . (C(u,c) /\ C(v,d) -> (c != d))
such that
  t in C
such that
  t[1] = t[2]
"""

parser = ep.EssenceParser()
rootTree = parser.parse(test_strings,"Test-spec")
ep.printTree(rootTree, printInfo=True)

json_data = json.dumps(rootTree, default=lambda o: o.__dict__)
print(json_data)
with open('testSpec.json', 'w') as f:
    f.write(json_data)

g = ep.getNXTree("Test-spec", rootTree.children)
data = json_graph.node_link_data(g)

with open('specToNX.json', 'w') as f:
    json.dump(data,f)


def read_json_file(filename):
    with open(filename) as f:
        js_graph = json.load(f)
    return json_graph.node_link_graph(js_graph)

file = read_json_file('specToNX.json')
print(file.nodes())