import ETransformulator as ET
import GP2Graph
import networkx as nx
from inspect import signature
import matplotlib.pyplot as plt
import time
import collections
import random

class ETGraph:
    '''
    Container for the networkx transformulator graph. Each vertex is a form, each edge a function that takes an Emini specification from one form to another. 
    Each edge contains a callable function in its "func" attribute automatically extracted from the ET python script
    '''
    def __init__(self):
        self.formsGraph = nx.DiGraph()

        for val in ET.__dict__.values():
            if(callable(val)):
                fromTo = val.__name__.split('To')
                self.formsGraph.add_edge(fromTo[0],fromTo[1], func = val)

    def FormToForm(self, AST, fromForm, toForm):

        ETpath = nx.shortest_path(self.formsGraph, source=fromForm, target=toForm)
        for formIndex in range(0,len(ETpath)-1):
            AST = self.formsGraph[ETpath[formIndex]][ETpath[formIndex+1]]["func"](AST)

        return AST

    def eulerTour(self, AST, origin):
        '''
        perform all the evailable conversion and returns to the original form if the graph is eulerian
        '''
        eulerCircuit = nx.eulerian_circuit(self.formsGraph, origin)
        for transformulation in eulerCircuit:
            AST = transformulation(AST)

        return AST
    
    def TimedEulerTour(self, AST, origin):

        timeGraph = nx.DiGraph()
        timeGraph.name = AST
        eulerCircuit = nx.eulerian_circuit(self.formsGraph, origin)
        for transformulation in eulerCircuit:
            start = time.time_ns() 
            AST = transformulation(AST)            
            end = time.time_ns() 
            timeGraph.add_edge(*transformulation, time = end - start)
        return AST, timeGraph
    
    def timedCycle(self, AST, origin):

        timeGraph = nx.DiGraph()
        timeGraph.name = AST
        cycle = nx.find_cycle(self.formsGraph, origin)

        for transformulation in cycle:
            start = time.time_ns() 
            #print(transformulation)
            AST = self.formsGraph.get_edge_data(*transformulation)["func"](AST)
            #print(AST)          
            end = time.time_ns() 
            timeGraph.add_edge(*transformulation, time = end - start)
        return AST, timeGraph
    
    def timedCyclesTours(self, AST, origin):

        timeGraph = nx.DiGraph()
        timeGraph.name = AST
        cycles = nx.simple_cycles(self.formsGraph)
        print(cycles)
        for cycle in cycles:
            if origin in cycle:
                print(cycle)
                offset = cycle.index(origin) 
                print(offset)
                cycle = collections.deque(cycle)
                cycle.rotate(-offset) # make sure the first form is the origin
                print(cycle)
                for formIndex in range(0,len(cycle)):
                    start = time.time_ns() 
                    #print(transformulation)
                    toIndex = (formIndex+1)%len(cycle)
                    AST = self.formsGraph[cycle[formIndex]][cycle[toIndex]]["func"](AST)
                    #print(AST)          
                    end = time.time_ns() 
                    timeGraph.add_edge(cycle[formIndex],cycle[toIndex], time = end - start)
        return AST, timeGraph
            
    def allPathsFrom(self, AST, origin):

        timeGraph = nx.DiGraph()
        timeGraph.name = AST
        paths = nx.single_source_shortest_path(self.formsGraph, origin)

        for path in paths.values():

            AST = timeGraph.name       
            for formIndex in range(0,len(path)-1):
                start = time.time_ns() 
                #print(transformulation)
                toIndex = formIndex+1
                AST = self.formsGraph[path[formIndex]][path[toIndex]]["func"](AST)
                #print(AST)          
                end = time.time_ns() 
                timeGraph.add_edge(path[formIndex],path[toIndex], time = end - start)
        return AST, timeGraph
    
    def allEdgesFrom(self, AST, origin):

        timeGraph = nx.DiGraph()
        timeGraph.name = AST
        paths = nx.single_source_shortest_path(self.formsGraph, origin)

        for path in paths.values():

            AST = timeGraph.name       
            for formIndex in range(0,len(path)-1):
                start = time.time_ns() 
                #print(transformulation)
                toIndex = formIndex+1
                AST = self.formsGraph[path[formIndex]][path[toIndex]]["func"](AST)
                #print(AST)          
                end = time.time_ns() 
                timeGraph.add_edge(path[formIndex],path[toIndex], time = end - start)
            newSource = AST
            if len(path) > 1:
                print(list(self.formsGraph.neighbors(path[-1])))
                for neighbour in list(self.formsGraph.neighbors(path[-1])):
                    
                    start = time.time_ns() 
                    #print(transformulation)
                    tg =self.formsGraph[path[-1]][neighbour]["func"](newSource)        
                    end = time.time_ns() 
                    timeGraph.add_edge(path[-1],neighbour, time = end - start)
                    print(tg)
        return AST, timeGraph
    
    def heuristicChinesePostman(self, AST, origin):
        '''
        Poor man heuristic to solve the the chinese postman problem.
        We need a closed cycle that passes over each edge at least once. It is ok if more than once.
        Likely suboptical.

        create stack of edges in the graph
        start from origin. 
        while there are elements in the stack
            pick an edge in the stack
            compute shortest path to target of edge
            traverse the path transforming the AST with each step and remove all edges encoundered on the way from the stack
        when stack is empty return to origin
        '''
        if not nx.is_strongly_connected(self.formsGraph):
            raise ValueError("Unreachable nodes in the graph")
        
        unvisitedEdges = []
        [unvisitedEdges.append(edge) for edge in self.formsGraph.edges()]
        currentNode = origin
        cycle = []
        cycle.append(origin)

        while len(unvisitedEdges) > 0:
            targetEdge = random.choice(unvisitedEdges)
            ETpath = nx.shortest_path(self.formsGraph, source=currentNode, target=targetEdge[1])
            
            for formIndex in range(0,len(ETpath)-1):
               # print("FROM " +ETpath[formIndex]+ " TO " + ETpath[formIndex+1] )
                #print(AST)
                #if type(AST) == ET.ep.Node:
                    #print(ET.ep.printTree(AST,printInfo=True))
                AST = self.formsGraph[ETpath[formIndex]][ETpath[formIndex+1]]["func"](AST)
                if (ETpath[formIndex],ETpath[formIndex+1]) in unvisitedEdges:
                    unvisitedEdges.remove((ETpath[formIndex],ETpath[formIndex+1]))                
                cycle.append(ETpath[formIndex+1])
                
            currentNode = targetEdge[1]

        if currentNode == origin:
            return AST,cycle
        else:
            ETpath = nx.shortest_path(self.formsGraph, source=currentNode, target=origin)
            for formIndex in range(0,len(ETpath)-1):
                AST = self.formsGraph[ETpath[formIndex]][ETpath[formIndex+1]]["func"](AST)           
                cycle.append(ETpath[formIndex+1])

        return AST,cycle


def funcTests():
    teststr = """
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

    ast = ET.EminiToASTpy(teststr)
    ETG = ETGraph()

    ast2= ETG.allEdgesFrom(ast,"ASTpy")
    #print(ast2[0])
    G= ast2[1]
    #print(ET.ASTpyToEmini(ast2[0]))
    edge_labels = nx.get_edge_attributes(G,'time')
    #print(edge_labels)

    pos = nx.circular_layout(G)
    #nx.draw(G, pos,with_labels=True)
    #nx.draw_networkx_nodes(G, pos, with_labels=True)
    #node_labels = nx.get_node_attributes(G, "label")
    #nx.draw_networkx_labels(G, pos, labels = node_labels)

    nx.draw_networkx_edge_labels(G,pos, labels = edge_labels,label_pos=0.3)

    nx.draw_circular(G,with_labels=True, node_size=300, connectionstyle="arc3,rad=-0.1" )
    plt.show()

def postMantest():
    teststr = """
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

    ast = ET.EminiToASTpy(teststr)
    ETG = ETGraph()
    
    newAst, cycle = ETG.heuristicChinesePostman(ast,"ASTpy")
    pos = nx.circular_layout(ETG.formsGraph)
    #nx.draw(G, pos,with_labels=True)
    #nx.draw_networkx_nodes(G, pos, with_labels=True)
    #node_labels = nx.get_node_attributes(G, "label")
    #nx.draw_networkx_labels(G, pos, labels = node_labels)
    path_edges = list(zip(cycle,cycle[1:]))
    print(cycle)
    nx.draw(ETG.formsGraph,pos, with_labels=True)

    path_edges = list(zip(cycle,cycle[1:]))
    #nx.draw_networkx_nodes(ETG.formsGraph,pos,nodelist=cycle,node_color='r')
    nx.draw_networkx_edges(ETG.formsGraph,pos,edgelist=path_edges,edge_color='g',alpha=0.3,width=2,connectionstyle="arc3,rad=-0.1")
    plt.show()

#postMantest()