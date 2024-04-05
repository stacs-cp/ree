import sys
sys.path.append('.')
import EFormatConverters as EFC
import EFormatGraph as EFG
import gp2Graph
import networkx as nx
from inspect import signature
import matplotlib.pyplot as plt
from matplotlib.pyplot import text

import math
from networkx.drawing.nx_pydot import graphviz_layout
#from karateclub import FeatherGraph ## Prune
#forms = ["EminiSpec","ASTpy","1DTokens","ASTNX","ASTpyJson","GP2Graph","Neo4j"]
import pandas as pd
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

    srd = 0.7 # Second ring distance

    formsGraph.add_node("Conjure")
    formsGraph.add_edge("Emini", "Conjure", color='#FF5342')
    formsGraph.add_edge("Conjure", "Emini", color='#FF5342')
    polarPos = polar(pos["Emini"][0],pos["Emini"][1])
    print(polarPos)
    conjurePos = polarToCartesian(polarPos[0]+srd,polarPos[1])
    pos["Conjure"] = conjurePos

    for p in pos:
        tempPos = pos[p]
        tempPoral = polar(*tempPos)
        pos[p] = polarToCartesian(tempPoral[0],tempPoral[1]+60)
        print()


    formsGraph.add_node("GP2")
    formsGraph.add_edge("GP2String", "GP2", color ='#006C84')
    formsGraph.add_edge("GP2", "GP2String", color ='#006C84')

    formsGraph.add_edge("GP2StringDT", "GP2", color ='#006C84')
    formsGraph.add_edge("GP2", "GP2StringDT", color ='#006C84')

    polarPos = polar(pos["GP2String"][0],pos["GP2String"][1])
    GP2Pos = polarToCartesian(polarPos[0]+srd, polarPos[1])
    pos["GP2"] = GP2Pos


    mapping = {"Emini": "Essence", "ASTpy": "AST", "GP2String": "GP2\nString", "GP2Graph": "GP2\nGraph", "GP2StringDT":"GP2\nString\nDT"}
    formsGraph = nx.relabel_nodes(formsGraph,mapping)
    pos["Essence"] = pos["Emini"]
    pos["GP2\nString"] = pos["GP2String"]
    pos["GP2\nString\nDT"] = pos["GP2StringDT"]
    pos["GP2\nGraph"] = pos["GP2Graph"]
    pos["AST"] = pos["ASTpy"]
    pos.pop("Emini")
    pos.pop("GP2Graph")
    pos.pop("GP2String")
    pos.pop("ASTpy")
    pos.pop("GP2StringDT")

    figure, axes = plt.subplots(figsize=(12,9))

    Drawing_uncolored_circle = plt.Circle( (0.0, 0.0 ),
                                        1.0 ,
                                        alpha=1.0,
                                        color='#174D7C',
                                        zorder=0)

    axes.set_aspect('equal')

    figure.tight_layout()
    #plt.gca().legend(('y0','y1'))
    from matplotlib.patches import Patch,FancyArrowPatch
    #legend_elements = [plt.Line2D([0], [0], marker='_', color='y', linestyle="-",markeredgecolor="b",label='Semantically idempotent translations')]
    legend_elements = [FancyArrowPatch((0,0),(0,0),facecolor='white', edgecolor='#174D7C',label='Formats Translations'),
                    Patch(facecolor='#FF5342', label='Conjure API'),
                    Patch(facecolor='#006C84', label='GP2 API')]

                    
    axes.legend(handles=legend_elements, loc='lower left')
    colors = nx.get_edge_attributes(formsGraph,'color').values()
    axes.add_artist( Drawing_uncolored_circle )

    nx.draw(formsGraph, pos, with_labels=False,edge_color=colors, node_size=4900, width=5,connectionstyle="arc3,rad=-0.1", ax=axes)
    for node, (x, y) in pos.items():
        text(x, y, node, fontsize=18, ha='center', va='center')
    nodes = nx.draw_networkx_nodes(formsGraph, pos,node_color='#ffffff', node_size=5500)
    nodes.set_edgecolor('#819898')
    plt.savefig("ICGT2024map2.png")
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


def bigGridPlot():
    import eminigen
    fig, axs = plt.subplots(10, 10, figsize=(20, 20))
    Gs = []
    for i, ax_row in enumerate(axs):
        for j, ax in enumerate(ax_row):
            spec = eminigen.spawnEssence()
            efg = EFG.EFGraph()
            g = efg.FormToForm(spec,"Emini","NX")
            h = g.to_undirected()
            Gs.append(g)
            colours_map = []
            for node in g.nodes(data=True):
                #print(node)
                if node[1]['info'] == 'BinaryExpression':
                    colours_map.append('red')
                elif node[1]['info'] == 'FindStatement':
                    colours_map.append('navy')
                elif node[1]['info'] == 'NameLettingStatement':
                    colours_map.append('orchid')
                else:
                    colours_map.append("blue")

            nx.draw(h, nx.fruchterman_reingold_layout(h,iterations = 450),node_color=colours_map, node_size=15, ax=ax)  

            ax.set_xticks([])
            ax.set_yticks([])
            #if i == 0:
            #    ax.set_title(f"mod{j}", size=3)
            #if j == 0:
            #    ax.set_ylabel(f"repetitions {i}", size=3)
            #ax.set_facecolor("navy")
    #fig.set_facecolor('navy')
    #fig.suptitle("PaC-MAP Embedding of TSP instances", y=0.92, size=20)
    
    #plt.subplots_adjust(wspace=0.05, hspace=0.05)
    fig.tight_layout()

    plt.show()

    for i in range(300):
        spec = eminigen.spawnEssence()
        efg = EFG.EFGraph()
        g = efg.FormToForm(spec,"Emini","NX")
        h = g.to_undirected()
        Gs.append(g)

    model = FeatherGraph()
    model.fit(Gs)
    X = model.get_embedding()
    embedding = umap.UMAP(n_neighbors=20,
                      n_components=4,
                      min_dist=1,
                      metric='correlation').fit_transform(X)
    fig2 = plt.figure(figsize=(200,200))


    plt.scatter(embedding[:, 0], embedding[:, 1],
                edgecolor='none',
                alpha=0.80,
                s=14)
    plt.axis('off');
    fig2.tight_layout()
    plt.show()

#bigGridPlot()
MainTMAP()  
#
#timedMaps()
