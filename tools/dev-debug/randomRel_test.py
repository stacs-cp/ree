import sys
sys.path.append('../ree/tools')
import eminipyparser as ep
import instaGen
import EFormatGraph
import networkx as nx


rndG = nx.gnm_random_graph(5,10)
print(instaGen.NXtoEssenceRelation(rndG))