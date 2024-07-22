import sys
sys.path.append('.')

from greee import instaGen
import networkx as nx
test_string = ""

test_graph = nx.gnm_random_graph(40,120)
#test_graph = nx.dodecahedral_graph()
#test_graph = nx.ring_of_cliques(2,5)
print(*test_graph.edges(data=False))
test_string += instaGen.NXtoEssenceRelationForGCmulti(test_graph, "n","edges") + " \n"
test_string += "letting numberColours be 10 \n"
test_string += "letting coloursPerNode be 2 \n"

print(test_string)
graphcolouring_file = "tests/gcmulti_cliq5-6-2.param"
with open(graphcolouring_file, 'w') as file:
    file.write(test_string)
