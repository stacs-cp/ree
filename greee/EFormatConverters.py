"""
This module contains a set of conversions between formats for the Abstract Syntax Tree of an Emini specification.
The name of the functions should follow the pattern Format1ToFormat2. The word "To" is used as a splitter by other functions, currently EFormatGraph, that automatically
grabs all functions in this script. At this point in time having the substring "To" in one of the names will cause issues.
"""

from greee import eminipyparser as ep
import networkx as nx
from greee import gp2Graph
from greee import icing
import json
import re
import random

def EminiToASTpy(spec, specname="unnamed"):
    '''
    Turns an Essence-Mini specification (string) into an Abstract Syntax Tree of python objects.
    '''
    parser = ep.EssenceParser()
    ASTpy = parser.parse(spec, specname)
    return ASTpy

def ASTpyToEmini(ASTpy):
    '''
    Turns an Abstract Syntax Tree of python objects into an Essence-Mini specification (string). 
    '''
    return icing.ASTtoEssence(ASTpy)


def ASTpyToJson(ASTpy):
    '''
    Turns an Abstract Syntax Tree of python objects into JSON format.
    '''
    return json.dumps(ASTpy, default=lambda o: o.__dict__)

def JsonToASTpy(jsonString):
    '''
    Turns a JSON String of an AST into an Abstract Syntax Tree of python objects.
    '''  
    ASTpy = json.loads(jsonString, object_hook=lambda ASTpy: ep.Node(**ASTpy))
    return ASTpy

def ASTpyToGP2Graph(ASTpy):
    '''
    Turns an Abstract Syntax Tree of python objects into a Graph mapped to the GP2 format.
    '''
    gp2g = gp2Graph.Graph([],[])
    
    def buildTree(node, Tree, index=1, parentID=None):   
        nodeID = len(gp2g.nodes)             
        Tree.addNode(nodeID, node.label,node.info) 
        if parentID != None: 
            edgeID = len(gp2g.edges)
            Tree.addEdge(edgeID,parentID,nodeID,index)
        for i in range(len(node.children)):
            buildTree(node.children[i], Tree, i+1, nodeID)
    
    buildTree(ASTpy,gp2g)
    return gp2g

# under maintenance. create ASTpy via NX in the meantime
#def GP2GraphToASTpy(gp2graph):
#    '''
#    Turns a Graph mapped to the GP2 format to Abstract Syntax Tree of python objects. ROOT must be node 0 
#    This is O(V*E) time. TODO: Loop over edges instead of the nodes and produce adjacency list first.
#    '''
#
#    def buildNode(gp2vertex):   
#    
#        vertex = gp2vertex[1].split('~')
#        label = vertex[0]
#        info = vertex[1]
#        edges = [edge for edge in gp2graph.edges if edge[1] == gp2vertex[0]] # create list of all the targets in the edges where the node is the source
#        sorted_edges = sorted(edges, key=lambda x:int(x[3]))  # sort based on index label (4th element of an edge in GP2 format)
#        children = []
#        for target in sorted_edges:
#            children.append(buildNode(gp2graph.nodes[int(target[2])]))
#        node = ep.Node(label,children,info)
#
#        return node
#
#    gp2graph.nodes = sorted(gp2graph.nodes, key=lambda x:int(x[0])) # nodes are sorted to ensure root is first
#    ASTpy = buildNode(gp2graph.nodes[0])
#    return ASTpy

def GP2GraphToNX(gp2graph):
    '''
    Returns a NetworkX tree graph from a GP2Graph python objects.
    '''
    G = nx.DiGraph()
    
    for node in gp2graph.nodes:
        #vertex = node[1].split('~')
        label = gp2Graph.ToEssenceHelper(node[1])
        info = node[2]               
        G.add_node(node[0], label = label, info=info)
    for edge in gp2graph.edges:
        G.add_edge(edge[1], edge[2], ID=edge[0], index= edge[3])
    #print(G.nodes)
    return G


def ASTpyToNX(ASTpy):
    '''
    Returns a NetworkX tree graph from an Abstract Syntax Tree of python objects.
    '''
    G = nx.DiGraph()
    def buildTreeNX(node, Tree, index=1, parentID=None): 
        nodeID = len(G.nodes())                
        Tree.add_node(nodeID, label = node.label, info=node.info) 
        if parentID != None: 
            edgeID = len(G.edges())
            Tree.add_edge(parentID, nodeID, ID=edgeID, index=index)
        for i in range(len(node.children)):
            buildTreeNX(node.children[i], Tree, i+1, nodeID)

    buildTreeNX(ASTpy, G)
    return G

def NXToASTpy(NXGraph):
    '''
    From networkx to ASTpy.
    '''
    
    def buildNode(vertex, G): 
       
       # Sort node's children according to the index attribute stored in the edge
        neighbours = sorted(G[vertex].items(), key=lambda edge: int(edge[1]['index']))

        children = []
        for neighbour in neighbours:
            child = neighbour[0]
            children.append(buildNode(child,G))
        node = ep.Node(G.nodes[vertex]['label'],children,G.nodes[vertex]['info'])
        return node

    root = list(nx.topological_sort(NXGraph))[0]
    #print(root)
    ASTpy = buildNode(root, NXGraph)
    return ASTpy
    


def NXToGP2Graph(NXGraph):
    '''
    Converts a NetworkX Graph into a GP2Graph.
    '''
    gp2graph = gp2Graph.Graph([],[])
    for id,node in NXGraph.nodes(data=True):
        label = node['label']
        info = node['info']
        gp2graph.addNode(id,label,info)
    for u,v,data in NXGraph.edges(data=True):
        gp2graph.addEdge(data['ID'],u,v,data['index'])

    return gp2graph

    


def GP2GraphToGP2String(GP2Graph):
    '''
    Produce a GP2 representation of the graph in string format.
    '''
    #random.shuffle(GP2Graph.nodes) #TODO seed with parameter
    GP2String = ""
    GP2String += "[\n"
    for node in GP2Graph.nodes:
        GP2String += f'({node[0]},\"{node[1]}~{node[2]}\")\n'
    GP2String += "| \n"
    for edge in GP2Graph.edges:
        GP2String += f'({edge[0]},{edge[1]},{edge[2]},{edge[3]})\n'
    GP2String += "]"
    return GP2String   

### single trees, 2 double glued trees, ASG

def GP2GraphToGP2StringDT(GP2Graph):
    '''
    Produce a GP2 representation of the graph in string format.
    '''
    #random.shuffle(GP2Graph.nodes) #TODO seed with parameter
    ID_shift = len(GP2Graph.nodes)
    ID_shift_e = len(GP2Graph.edges)
    GP2String_DT = ""
    GP2String_DT += "[\n"
    info_edges_DT = ""
    for i,node in enumerate(GP2Graph.nodes):
        if type(node[0]) == str:
            print(node[0])
        nodeid = int(node[0])
        GP2String_DT += f'({nodeid},\"{node[1]}")\n'
        GP2String_DT += f'({nodeid+ID_shift},\"{node[2]}\")\n'
        info_edges_DT+= f'({i+ID_shift_e*2},{nodeid},{nodeid+ID_shift}, \"info\")\n'
    GP2String_DT += "| \n"
    for edge in GP2Graph.edges:
        GP2String_DT += f'({edge[0]},{edge[1]},{edge[2]},{edge[3]})\n'
        GP2String_DT += f'({int(edge[0])+ID_shift_e},{int(edge[1])+ID_shift},{int(edge[2])+ID_shift},{edge[3]})\n'

    GP2String_DT += info_edges_DT
    GP2String_DT += "]"
    return GP2String_DT   

def GP2GraphToGP2StringB(GP2Graph):
    '''
    Produce a GP2 representation of the graph in string format.
    '''
    #random.shuffle(GP2Graph.nodes) #TODO seed with parameter
    ID_shift = len(GP2Graph.nodes)
    ID_shift_e = len(GP2Graph.edges)
    GP2String_B = ""
    GP2String_B += "[\n"
    info_edges_B = ""
    for i,node in enumerate(GP2Graph.nodes):
        if type(node[0]) == str:
            print(node[0])
        nodeid = int(node[0])
        GP2String_B += f'({nodeid},\"{node[1]}")\n'
        GP2String_B += f'({nodeid+ID_shift},\"{node[2]}\")\n'
        info_edges_B+= f'({i+ID_shift_e*2},{nodeid},{nodeid+ID_shift}, 0)\n'
    GP2String_B += "| \n"
    for edge in GP2Graph.edges:
        GP2String_B += f'({edge[0]},{edge[1]},{edge[2]},{edge[3]})\n'
        #GP2String_B += f'({int(edge[0])+ID_shift_e},{int(edge[1])+ID_shift},{int(edge[2])+ID_shift},{edge[3]})\n'

    GP2String_B += info_edges_B
    GP2String_B += "]"
    return GP2String_B   
###

def GP2StringDTToNX(gp2stringDT):
    '''
    Create graph object from gp2 formatted string . 
    '''
    gp2graph = gp2Graph.Graph([],[])
    tempG = nx.DiGraph()

    graphStarts =  [match.start() for match in re.finditer(r'\[', gp2stringDT)]
    if len(graphStarts) != 1:
        raise Exception("Some issue parsing [ found "+ str(len(graphStarts)))
    leftParentheses = [match.start() for match in re.finditer(r'\(', gp2stringDT)]
    rightParentheses = [match.start() for match in re.finditer(r'\)', gp2stringDT)]
    if len(leftParentheses) != len(rightParentheses):
        raise Exception("Number of ( does not match number of ): " + str(len(leftParentheses))+ "-" + str(len(rightParentheses)))
    
    nodeEdgeDivider = [match.start() for match in re.finditer(r'\|', gp2stringDT)]
    if len(nodeEdgeDivider) != 1:
        raise Exception("Some issue parsing | found: " +str(len(nodeEdgeDivider))) ## THIS WILL BREAK When we start parsing essence absolute value and list comprehensions

    graphEnds = [match.start() for match in re.finditer(r'\]', gp2stringDT)]
    if len(graphEnds) != 1:
        raise Exception("Some issue parsing ] found: " +str(len(graphEnds)))
    
    if len(leftParentheses) == 0:
        return "NullGraph"
    
    # parse nodes
    index =0
    while index < len(rightParentheses) and rightParentheses[index] < nodeEdgeDivider[0]:
        ## BUG removing "strip" from the line below bricks the converter, while adding strip add inconsist spaces which makes the syntactic equality check fail (but semantic equality is preserved)
        node = tuple([s.replace("\"","").strip() for s in gp2stringDT[leftParentheses[index]+1:rightParentheses[index]].split(',')])         
        if len(node) != 2:
            raise Exception("Some issue parsing nodes, found this node: " + str(node))
        else:
            tempG.add_node(node[0],value=node[1])
            #nodeLabelInfo = node[1].split("~")
            #gp2graph.nodes.append((node[0],nodeLabelInfo[0],nodeLabelInfo[1]))
        if index < len(rightParentheses): index += 1  ## if saveguards the case in which there are no edges in the spec
    
    # parse edges
    while index < len(rightParentheses):
        edge = tuple(s.strip() for s in gp2stringDT[leftParentheses[index]+1:rightParentheses[index]].split(','))
        if len(edge) != 4:
            raise Exception("Some issue parsing edges, found this edges: " + str(edge))
        else:
            gp2graph.edges.append(edge)
            tempG.add_edge(edge[1], edge[2], ID=edge[0], index= edge[3])

        index += 1
    
    G = nx.DiGraph()
    
    for edge in tempG.edges(data=True):
        if edge[2]['index'] == '"info"':
            e_label = gp2Graph.ToEssenceHelper(tempG.nodes[edge[0]]['value'])
            G.add_node(edge[0], label=e_label, info=tempG.nodes[edge[1]]['value'])
            out_edges = tempG.out_edges(edge[0],data=True)

            for e in out_edges:
                if e[2]['index'] != '"info"':
                    G.add_edge(e[0], e[1], ID=e[2]['ID'], index= e[2]['index'])
    return G


def GP2StringBToNX(gp2stringB):
    '''
    Create graph object from gp2 formatted string . 
    '''
    gp2graph = gp2Graph.Graph([],[])
    tempG = nx.DiGraph()

    graphStarts =  [match.start() for match in re.finditer(r'\[', gp2stringB)]
    if len(graphStarts) != 1:
        raise Exception("Some issue parsing [ found "+ str(len(graphStarts)))
    leftParentheses = [match.start() for match in re.finditer(r'\(', gp2stringB)]
    rightParentheses = [match.start() for match in re.finditer(r'\)', gp2stringB)]
    if len(leftParentheses) != len(rightParentheses):
        raise Exception("Number of ( does not match number of ): " + str(len(leftParentheses))+ "-" + str(len(rightParentheses)))
    
    nodeEdgeDivider = [match.start() for match in re.finditer(r'\|', gp2stringB)]
    if len(nodeEdgeDivider) != 1:
        raise Exception("Some issue parsing | found: " +str(len(nodeEdgeDivider))) ## THIS WILL BREAK When we start parsing essence absolute value and list comprehensions

    graphEnds = [match.start() for match in re.finditer(r'\]', gp2stringB)]
    if len(graphEnds) != 1:
        raise Exception("Some issue parsing ] found: " +str(len(graphEnds)))
    
    if len(leftParentheses) == 0:
        return "NullGraph"
    
    # parse nodes
    index =0
    while index < len(rightParentheses) and rightParentheses[index] < nodeEdgeDivider[0]:
        ## BUG removing "strip" from the line below bricks the converter, while adding strip add inconsist spaces which makes the syntactic equality check fail (but semantic equality is preserved)
        node = tuple([s.replace("\"","").strip() for s in gp2stringB[leftParentheses[index]+1:rightParentheses[index]].split(',')])         
        if len(node) != 2:
            raise Exception("Some issue parsing nodes, found this node: " + str(node))
        else:
            tempG.add_node(node[0],value=node[1])
            #nodeLabelInfo = node[1].split("~")
            #gp2graph.nodes.append((node[0],nodeLabelInfo[0],nodeLabelInfo[1]))
        if index < len(rightParentheses): index += 1  ## if saveguards the case in which there are no edges in the spec
    
    # parse edges
    while index < len(rightParentheses):
        edge = tuple(s.strip() for s in gp2stringB[leftParentheses[index]+1:rightParentheses[index]].split(','))
        if len(edge) != 4:
            raise Exception("Some issue parsing edges, found this edges: " + str(edge))
        else:
            gp2graph.edges.append(edge)
            tempG.add_edge(edge[1], edge[2], ID=edge[0], index= edge[3])

        index += 1
    
    G = nx.DiGraph()
    
    for edge in tempG.edges(data=True):
        if edge[2]['index'] == 0:
            e_label = gp2Graph.ToEssenceHelper(tempG.nodes[edge[0]]['value'])
            G.add_node(edge[0], label=e_label, info=tempG.nodes[edge[1]]['value'])
            out_edges = tempG.out_edges(edge[0],data=True)

            for e in out_edges:
                if e[2]['index'] != 0:
                    G.add_edge(e[0], e[1], ID=e[2]['ID'], index= e[2]['index'])
    return G



def GP2StringToGP2Graph(gp2string):
    '''
    Create graph object from gp2 formatted string . 
    '''
    gp2graph = gp2Graph.Graph([],[])

    graphStarts =  [match.start() for match in re.finditer(r'\[', gp2string)]
    if len(graphStarts) != 1:
        raise Exception("Some issue parsing [ found "+ str(len(graphStarts)))
    leftParentheses = [match.start() for match in re.finditer(r'\(', gp2string)]
    rightParentheses = [match.start() for match in re.finditer(r'\)', gp2string)]
    if len(leftParentheses) != len(rightParentheses):
        raise Exception("Number of ( does not match number of ): " + str(len(leftParentheses))+ "-" + str(len(rightParentheses)))
    
    nodeEdgeDivider = [match.start() for match in re.finditer(r'\|', gp2string)]
    if len(nodeEdgeDivider) != 1:
        raise Exception("Some issue parsing | found: " +str(len(nodeEdgeDivider))) ## THIS WILL BREAK When we start parsing essence absolute value and list comprehensions

    graphEnds = [match.start() for match in re.finditer(r'\]', gp2string)]
    if len(graphEnds) != 1:
        raise Exception("Some issue parsing ] found: " +str(len(graphEnds)))
    
    if len(leftParentheses) == 0:
        return "NullGraph"
    
    # parse nodes
    index =0
    while index < len(rightParentheses) and rightParentheses[index] < nodeEdgeDivider[0]:
        ## BUG removing "strip" from the line below bricks the converter, while adding strip add inconsist spaces which makes the syntactic equality check fail (but semantic equality is preserved)
        node = tuple([s.replace("\"","").strip() for s in gp2string[leftParentheses[index]+1:rightParentheses[index]].split(',')])         
        if len(node) != 2:
            raise Exception("Some issue parsing nodes, found this node: " + str(node))
        else:
            nodeLabelInfo = node[1].split("~")
            gp2graph.nodes.append((node[0],nodeLabelInfo[0],nodeLabelInfo[1]))
        if index < len(rightParentheses): index += 1  ## if saveguards the case in which there are no edges in the spec
    
    # parse edges
    while index < len(rightParentheses):
        edge = tuple(s.strip() for s in gp2string[leftParentheses[index]+1:rightParentheses[index]].split(','))
        if len(edge) != 4:
            raise Exception("Some issue parsing edges, found this edges: " + str(edge))
        else:
            gp2graph.edges.append(edge)
            
        index += 1

    return gp2graph
