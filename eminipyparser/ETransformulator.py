import eminipyparser as ep
import networkx as nx
import GP2Graph
import icing
import json

def EminiToASTpy(spec, specname="Root"):
    '''
    Turns an Essence-Mini specification (string) into an Abstract Syntax Tree of python objects 
    '''
    parser = ep.EssenceParser()
    statements = parser.parse(spec)
    ASTpy = ep.Node(specname , statements)
    return ASTpy

def ASTpyToEmini(ASTpy):
    '''
    Turns an Abstract Syntax Tree of python objects into an Essence-Mini specification (string) 
    '''
    return icing.ASTtoEssence(ASTpy)


def ASTpyToJson(ASTpy):
    '''
    Turns an Abstract Syntax Tree of python objects into JSON format
    '''
    return json.dumps(ASTpy, default=lambda o: o.__dict__)

def JsonToASTpy(json):
    '''
    Turns a JSON File of an AST into an Abstract Syntax Tree of python objects
    '''
    with open(json) as f:
        ASTpy = json.load(f, object_hook=lambda ASTpy: ep.Node(**ASTpy))
    return ASTpy

def ASTpyToGP2Graph(ASTpy):
    '''
    Turns an Abstract Syntax Tree of python objects into a Graph mapped to the GP2 format
    '''
    gp2g = GP2Graph.Graph([],[])
    
    def buildTree(node, Tree, index=1, parentID=None):   
        nodeID = len(gp2g.nodes)             
        Tree.addNode(nodeID, f'{node.label}#{node.info}') 
        if parentID != None: 
            edgeID = len(gp2g.edges)
            Tree.addEdge(edgeID,parentID,nodeID,index)
        for i in range(len(node.children)):
            buildTree(node.children[i], Tree, i+1, nodeID)
    
    buildTree(ASTpy,gp2g)
    return gp2g

def GP2GraphToASTpy(gp2graph):
    '''
    Turns a Graph mapped to the GP2 format to Abstract Syntax Tree of python objects. ROOT must be node 0 
    '''
    
    def buildNode(gp2vertex):   
    
        vertex = gp2vertex[1].split('#')
        label = vertex[0]
        info = vertex[1]
        edges = [edge for edge in gp2graph.edges if edge[1] == gp2vertex[0]] # create list of all the targets in the edges where the node is the source
        sorted_edges = sorted(edges, key=lambda x:x[3])  # sort based on index label (4th element of an edge in GP2 format)
        children = []
        for target in sorted_edges:
            children.append(buildNode(gp2graph.nodes[int(target[2])]))
        node = ep.Node(label,children,info)

        return node

    ASTpy = buildNode(gp2graph.nodes[0])
    return ASTpy


def ASTpyToNX(ASTpy):
    '''
    Returns a NetworkX tree graph from an Abstract Syntax Tree of python objects
    '''
    G = nx.DiGraph()
    def buildTreeNX(node, Tree, index=1, parentID=None): 
        nodeID = len(G.nodes())                
        Tree.add_node(nodeID, label = node.label, info=node.info) 
        if parentID != None: 
            edgeID = len(G.edges())
            Tree.add_edge(nodeID, parentID, ID=edgeID, index=index)
        for i in range(len(node.children)):
            buildTreeNX(node.children[i], Tree, i+1, nodeID)

    buildTreeNX(ASTpy, G)
    return G

def NXToASTpy(NXGraph):
    '''
    TODO From networkx to ASTpy
    '''
    root = [n for n,d in NXGraph.in_degree() if d==0] 
    successorList = nx.dfs_successors(NXGraph, source=root)
    AST = []
    
