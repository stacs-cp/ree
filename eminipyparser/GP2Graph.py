class Graph:
    def __init__(self, nodes = [], edges =[]):
        self.nodes = nodes
        self.edges = edges

    def addNode(self, ID,label="empty"):
        self.nodes.append((ID,label))

    def addEdge(self,ID,edgeFrom,edgeTo,label="empty"):
        self.edges.append((ID,edgeFrom,edgeTo,label))

    def getGP2String(self):
        '''
        Produce GP2 representation of the graph in string format
        '''
        gp2string = ""
        gp2string += "[\n"
        for node in self.nodes:
            gp2string += str(node)
        gp2string += "\n | \n"
        for edge in self.edges:
            gp2string += str(edge)
        gp2string += "\n]"
        return gp2string        
        
