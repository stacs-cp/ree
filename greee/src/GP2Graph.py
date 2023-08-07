import re

class Graph:
    def __init__(self, nodes = [], edges =[]):
        self.nodes = nodes
        self.edges = edges

    def addNode(self, ID,label="empty"):
        self.nodes.append((ID,label))

    def addEdge(self,ID,edgeFrom,edgeTo,label="empty"):
        self.edges.append((ID,edgeFrom,edgeTo,label))

    
        

