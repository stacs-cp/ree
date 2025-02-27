from greee import EFormatConverters as EFC
from greee import EFormatGraph as EFG
from greee import gp2Graph
import networkx as nx
from inspect import signature
import matplotlib.pyplot as plt
import math
from networkx.drawing.nx_pydot import graphviz_layout
#from karateclub import FeatherGraph ## Prune
#forms = ["EminiSpec","ASTpy","1DTokens","ASTNX","ASTpyJson","GP2Graph","Neo4j"]
import pandas as pd
#import umap.umap_ as umap
import numpy as np

def MainTMAP():
    '''
    Highly customised plot for ModRef2023
    '''
    formsGraph = nx.DiGraph()

    for val in EFC.__dict__.values():
        if(callable(val)):
            fromTo = val.__name__.split('To')
            formsGraph.add_edge(fromTo[0],fromTo[1], func = val.__name__, color='w')

    pos = nx.circular_layout(formsGraph)
    print(pos)   

    tempos = pos["Emini"]
    pos["Emini"] = pos["Json"] 
    pos["Json"] = tempos

    srd = 0.8 # Second ring distance

    formsGraph.add_node("Eprime")
    formsGraph.add_edge("Emini", "Eprime", color='#FF5342')
    polarPos = polar(pos["Emini"][0],pos["Emini"][1])
    EprimePos = polarToCartesian(polarPos[0]+srd,polarPos[1])
    pos["Eprime"] = EprimePos


    SavileRowOutputs = ["MiniZinc","FlatZinc","Minion","Gecode","SMT", "MaxSAT", "SAT"]

    separation = 10
    solversDist=0.7
    for i,output in enumerate(SavileRowOutputs):
        formsGraph.add_node(output)
        formsGraph.add_edge("Eprime",output,color='#FF9463')
        
        outputPos = polar(pos["Emini"][0],pos["Emini"][1])
        outputPos = polarToCartesian(outputPos[0]+srd+solversDist, outputPos[1]-(len(SavileRowOutputs)*separation)/2+(i*separation))
        pos[output] = outputPos

    formsGraph.add_node("Athanor")
    formsGraph.add_edge("Emini", "Athanor", color='black')
    polarPos = polar(pos["Emini"][0],pos["Emini"][1])
    AthanorPos = polarToCartesian(polarPos[0]+srd+solversDist,polarPos[1]+(len(SavileRowOutputs)*separation)/2)
    pos["Athanor"] = AthanorPos 

    formsGraph.add_node("GP2")
    formsGraph.add_edge("GP2String", "GP2", color ='#006C84')
    polarPos = polar(pos["GP2String"][0],pos["GP2String"][1])
    GP2Pos = polarToCartesian(polarPos[0]+srd, polarPos[1])
    pos["GP2"] = GP2Pos

    formsGraph.add_node("ML")
    formsGraph.add_edge("NX", "ML", color ='black')
    polarPos = polar(pos["NX"][0],pos["NX"][1])
    GNNPos = polarToCartesian(polarPos[0]+srd, polarPos[1])
    pos["ML"] = GNNPos

    formsGraph.add_node("Comms")
    formsGraph.add_edge("Json", "Comms",color ='black')
    polarPos = polar(pos["Json"][0],pos["Json"][1])
    CommsPos = polarToCartesian(polarPos[0]+srd, polarPos[1])
    pos["Comms"] = CommsPos

    mapping = {"ASTpy": "EMini\nAST", "GP2String": "GP2\nString", "GP2Graph": "GP2\nGraph"}
    formsGraph = nx.relabel_nodes(formsGraph,mapping)
    pos["GP2\nString"] = pos["GP2String"]
    pos["GP2\nGraph"] = pos["GP2Graph"]
    pos["EMini\nAST"] = pos["ASTpy"]
    pos.pop("GP2Graph")
    pos.pop("GP2String")
    pos.pop("ASTpy")

    figure, axes = plt.subplots(figsize=(9,9))

    Drawing_uncolored_circle = plt.Circle( (0.0, 0.0 ),
                                        1.0 ,
                                        alpha=1.0,
                                        color='#174D7C',
                                        zorder=0)

    axes.set_aspect('equal')

    figure.tight_layout()
    #plt.gca().legend(('y0','y1'))
    from matplotlib.patches import Patch
    #legend_elements = [plt.Line2D([0], [0], marker='_', color='y', linestyle="-",markeredgecolor="b",label='Semantically idempotent translations')]
    legend_elements = [Patch(facecolor='white', edgecolor='#174D7C',label='New Formats Translations'),
                    Patch(facecolor='#FF5342', label='Conjure'),
                    Patch(facecolor='#FF9463', label='Savile Row'),
                    Patch(facecolor='#006C84', label='GP2 Compiler')]

                    
    axes.legend(handles=legend_elements, loc='lower left')
    colors = nx.get_edge_attributes(formsGraph,'color').values()
    axes.add_artist( Drawing_uncolored_circle )

    nx.draw(formsGraph, pos, with_labels=True,edge_color=colors, node_size=2400, width=3,connectionstyle="arc3,rad=-0.1", ax=axes)
    nodes = nx.draw_networkx_nodes(formsGraph, pos,node_color='#ffffff', node_size=2400)
    nodes.set_edgecolor('#819898')

    plt.show()


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

def expMapSkeleton():
    formsGraph = nx.DiGraph()

    for val in EFC.__dict__.values():
        if(callable(val)):
            fromTo = val.__name__.split('To')
            formsGraph.add_edge(fromTo[0],fromTo[1], func = val.__name__)

    pos = nx.circular_layout(formsGraph)

    #tempos = pos["Emini"]
    #pos["Emini"] = pos["Json"] 
    #pos["Json"] = tempos

    srd = 0.8 # Second ring distance

    secondRingMap = [("GP2String", "GP2"), ("Emini", "Eprime"),("NX", "ML"),("Json", "Comms")]

    for pair in secondRingMap:
        formsGraph.add_node(pair[1])
        formsGraph.add_edge(*pair)
        polarPos = polar(pos[pair[0]][0],pos[pair[0]][1])
        pos[pair[1]] = polarToCartesian(polarPos[0]+srd,polarPos[1])

    SavileRowOutputs = ["MiniZinc","FlatZinc","Minion","Gecode","SMT", "MaxSAT", "SAT"]

    separation = 10
    solversDist=0.7
    for i,output in enumerate(SavileRowOutputs):
        formsGraph.add_node(output)
        formsGraph.add_edge("Eprime",output,color='#FF9463')
        
        outputPos = polar(pos["Emini"][0],pos["Emini"][1])
        outputPos = polarToCartesian(outputPos[0]+srd+solversDist, outputPos[1]-(len(SavileRowOutputs)*separation)/2+(i*separation))
        pos[output] = outputPos

    formsGraph.add_node("Athanor")
    formsGraph.add_edge("Emini", "Athanor", color='black')
    polarPos = polar(pos["Emini"][0],pos["Emini"][1])
    AthanorPos = polarToCartesian(polarPos[0]+srd+solversDist,polarPos[1]+(len(SavileRowOutputs)*separation)/2)
    pos["Athanor"] = AthanorPos 

    mapping = {"ASTpy": "EMini\nAST", "GP2String": "GP2\nString", "GP2Graph": "GP2\nGraph"}
    formsGraph = nx.relabel_nodes(formsGraph,mapping)
    pos["GP2\nString"] = pos["GP2String"]
    pos["GP2\nGraph"] = pos["GP2Graph"]
    pos["EMini\nAST"] = pos["ASTpy"]
    pos.pop("GP2Graph")
    pos.pop("GP2String")
    pos.pop("ASTpy")

    figure, axes = plt.subplots(figsize=(9,9))

    Drawing_uncolored_circle = plt.Circle( (0.0, 0.0 ),
                                        1.0 ,
                                        alpha=1.0,
                                        facecolor='white',
                                        zorder=0,
                                        #linestyle='--',
                                        edgecolor='#174D7C')

    axes.set_aspect('equal')

    figure.tight_layout()
    #plt.gca().legend(('y0','y1'))
    from matplotlib.patches import Patch
    legend_elements = [plt.Line2D([0], [0], marker='_', color='y', linestyle="-",label='Path')]    

                    
    axes.legend(handles=legend_elements, loc='upper center')
    #colors = nx.get_edge_attributes(formsGraph,'color').values()
    axes.add_artist( Drawing_uncolored_circle )

    #,connectionstyle="arc3,rad=-0.1"
    nx.draw(formsGraph, pos, with_labels=True, node_size=2400, width=1, ax=axes)
    nodes = nx.draw_networkx_nodes(formsGraph, pos,node_color='#ffffff', node_size=2400)
    nodes.set_edgecolor('#819898')

    #plt.show()
    return formsGraph

def timedMaps():
    formsGraph = nx.DiGraph()

    for val in EFC.__dict__.values():
        if(callable(val)):
            fromTo = val.__name__.split('To')
            formsGraph.add_edge(fromTo[0],fromTo[1], func = val.__name__)

    pos = nx.circular_layout(formsGraph)

    tempos = pos["Emini"]
    pos["Emini"] = pos["Json"] 
    pos["Json"] = tempos

    srd = 0.8 # Second ring distance

    secondRingMap = [("GP2String", "GP2"), ("Emini", "Eprime"),("NX", "ML"),("Json", "Comms")]

    for pair in secondRingMap:
        formsGraph.add_node(pair[1])
        formsGraph.add_edge(*pair)
        polarPos = polar(pos[pair[0]][0],pos[pair[0]][1])
        pos[pair[1]] = polarToCartesian(polarPos[0]+srd,polarPos[1])

    SavileRowOutputs = ["MiniZinc","FlatZinc","Minion","Gecode","SMT", "MaxSAT", "SAT"]

    separation = 10;
    solversDist=0.7
    for i,output in enumerate(SavileRowOutputs):
        formsGraph.add_node(output)
        formsGraph.add_edge("Eprime",output,color='#FF9463')
        
        outputPos = polar(pos["Emini"][0],pos["Emini"][1])
        outputPos = polarToCartesian(outputPos[0]+srd+solversDist, outputPos[1]-(len(SavileRowOutputs)*separation)/2+(i*separation))
        pos[output] = outputPos

    formsGraph.add_node("Athanor")
    formsGraph.add_edge("Emini", "Athanor", color='black')
    polarPos = polar(pos["Emini"][0],pos["Emini"][1])
    AthanorPos = polarToCartesian(polarPos[0]+srd+solversDist,polarPos[1]+(len(SavileRowOutputs)*separation)/2)
    pos["Athanor"] = AthanorPos 

    mapping = {"ASTpy": "EMini\nAST", "GP2String": "GP2\nString", "GP2Graph": "GP2\nGraph"}
    formsGraph = nx.relabel_nodes(formsGraph,mapping)
    pos["GP2\nString"] = pos["GP2String"]
    pos["GP2\nGraph"] = pos["GP2Graph"]
    pos["EMini\nAST"] = pos["ASTpy"]
    pos.pop("GP2Graph")
    pos.pop("GP2String")
    pos.pop("ASTpy")

    figure, axes = plt.subplots(figsize=(9,9))

    Drawing_uncolored_circle = plt.Circle( (0.0, 0.0 ),
                                        1.0 ,
                                        alpha=1.0,
                                        facecolor='white',
                                        zorder=0,
                                        #linestyle='--',
                                        edgecolor='#174D7C')

    axes.set_aspect('equal')

    figure.tight_layout()
    #plt.gca().legend(('y0','y1'))
    from matplotlib.patches import Patch
    legend_elements = [plt.Line2D([0], [0], marker='_', color='red', linestyle="--",label='Transform and solve path')]    

                    
    axes.legend(handles=legend_elements, loc='upper center')
    #colors = nx.get_edge_attributes(formsGraph,'color').values()
    axes.add_artist( Drawing_uncolored_circle )

    #,connectionstyle="arc3,rad=-0.1"
    nx.draw(formsGraph, pos, with_labels=True, node_size=2400, width=1, ax=axes)
    nodes = nx.draw_networkx_nodes(formsGraph, pos,node_color='#ffffff', node_size=2400)
    nodes.set_edgecolor('#819898')

    tPath = nx.DiGraph()
    tPath.add_nodes_from(formsGraph.nodes())
    tPath.add_edge("Emini","EMini\nAST")
    tPath.add_edge("EMini\nAST","GP2\nGraph")
    tPath.add_edge("GP2\nGraph","GP2\nString")
    tPath.add_edge("GP2\nString","GP2")
    tPath.add_edge("GP2","GP2")
    tPath.add_edge("EMini\nAST","Emini")
    tPath.add_edge("GP2\nGraph","EMini\nAST")
    tPath.add_edge("GP2\nString","GP2\nGraph")
    tPath.add_edge("GP2","GP2\nString")
    tPath.add_edge("Emini","Eprime")
    tPath.add_edge("Eprime","Minion")
    tPath.add_edge("Minion","Minion")

    Drawing_red_circle = plt.Circle( pos["Emini"],
                                        0.211 ,
                                        alpha=1.0,
                                        facecolor='white',
                                        zorder=1,
                                        linewidth =2,
                                        #linestyle='--',
                                        edgecolor='red')

    axes.add_artist( Drawing_red_circle )
    #plt.show()
    #g = expMapSkeleton()
    nx.draw_networkx_edges(tPath,pos,edge_color='#CB4335',alpha=1,node_size=2400,width=3, style='--',connectionstyle="arc3,rad=-0.1")
    spec = '''
    find x : int(0..100)
    such that
        x > 1 * 2 + 3 * 4
        '''
    #spec = ""
    efg = EFG.EFGraph()

    #ast, timedGraph = efg.allPathsFrom(spec,"Emini")

    gp2s,timedGraph = efg.timedFormToForm(spec,"Emini","GP2String")
    print(timedGraph.edges(data=True))
    edge_weights = {(u, v): d['time'] for u, v, d in timedGraph.edges(data=True)}
    pos2 = nx.circular_layout(efg.formsGraph)
    #nx.draw_networkx_edges(timedGraph,pos2,edge_color='r',alpha=1,node_size=2400,width=3, style='--',connectionstyle="arc3,rad=-0.1")
    #texts = nx.draw_networkx_edge_labels(timedGraph, pos, edge_labels=edge_labels, label_pos=0.5, rotate=True)

    plt.show()

#bigGridPlot()
#MainTMAP()  <--this
#
#timedMaps()
