import re

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
        Produce a GP2 representation of the graph in string format
        '''
        gp2string = ""
        gp2string += "[\n"
        for node in self.nodes:
            gp2string += f'({node[0]},{node[1]})\n'
        gp2string += "| \n"
        for edge in self.edges:
            gp2string += f'({edge[0]},{edge[1]},{edge[2]},{edge[3]})\n'
        gp2string += "]"
        return gp2string   

    def graphFromGP2String(self, gp2string):
        '''
        Create graph object from gp2 formatted string . 
        '''
        self.nodes = []
        self.edges = []

        graphStarts =  [match.start() for match in re.finditer(r'\[', gp2string)]
        if len(graphStarts) != 1:
            raise Exception("Some issue parsing [ found"+ str(len(graphStarts)))
        leftParentheses = [match.start() for match in re.finditer(r'\(', gp2string)]
        rightParentheses = [match.start() for match in re.finditer(r'\)', gp2string)]
        if len(leftParentheses) != len(rightParentheses):
            raise Exception("Number of ( does not match number of ): " + str(len(leftParentheses))+ "-" + str(len(rightParentheses)))
        
        nodeEdgeDivider = [match.start() for match in re.finditer(r'\|', gp2string)]
        if len(nodeEdgeDivider) != 1:
            raise Exception("Some issue parsing | found: " +str(len(nodeEdgeDivider))) ## THIS WILL BREAK When we start parsing absolute essence absolute value and list comprehensions

        graphEnds = [match.start() for match in re.finditer(r'\]', gp2string)]
        if len(graphEnds) != 1:
            raise Exception("Some issue parsing ] found: " +str(len(graphEnds)))
        
        if len(leftParentheses) == 0:
            return "NullGraph"
        
        # parse nodes
        index =0
        while index < len(rightParentheses) and rightParentheses[index] < nodeEdgeDivider[0]:
            node = tuple([s.strip() for s in gp2string[leftParentheses[index]+1:rightParentheses[index]].split(',')])         
            if len(node) != 2:
                raise Exception("Some issue parsing nodes found this node: " + str(node))
            else:
                self.nodes.append(node)
            if index < len(rightParentheses): index += 1  ## if saveguards the case in which there are no edges in the spec
        
        # parse edges
        while index < len(rightParentheses):
            edge = tuple(s.strip() for s in gp2string[leftParentheses[index]+1:rightParentheses[index]].split(','))
            if len(edge) != 4:
                raise Exception("Some issue parsing edges found this edges: " + str(edge))
            else:
                self.edges.append(edge)
            index += 1
        

