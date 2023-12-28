"""
This module contains a set of conversions between formats for the Abstract Syntax Tree of an Emini specification.
The name of the functions should follow the pattern Format1ToFormat2. The word "To" is used as a splitter by other functions, currently EFormatGraph, that automatically
grabs all functions in this script. At this point in time having the substring "To" in one of the names will cause issues.
"""

import greee.eminipyparser as ep
import networkx as nx
import greee.GP2Graph as GP2Graph
import greee.icing
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
    gp2g = GP2Graph.Graph([],[])
    
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
        label = GP2Graph.ToEssenceHelper(node[1])
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
       
        def indexGetter(item):
            return int(item['index'])
        
        neighbours = sorted(G[vertex].items(), key=lambda edge: indexGetter(edge[1]))

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
    gp2graph = GP2Graph.Graph([],[])
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

def GP2StringToGP2Graph(gp2string):
    '''
    Create graph object from gp2 formatted string . 
    '''
    gp2graph = GP2Graph.Graph([],[])

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
