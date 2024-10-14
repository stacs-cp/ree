'''
Intermediate graph representation for GP2
'''
import re

class GP2Graph:
    '''
    Intermediate representation for GP2 that matches its graph descriptions.
    Vertices are tuples of indices and labels.
    Edges are quadruples of indices, source, target and labels'''
    def __init__(self, nodes = [], edges =[]):
        '''
        constructor
        '''
        self.nodes = nodes
        self.edges = edges

    def addNode(self, ID,label="empty",info = ""):
        """Add a node to the grpah

        Args:
            ID (int): Index of the node
            label (str, optional): Lexical Symbol. Defaults to "empty".
            info (str, optional): Syntactic information. Defaults to "".
        """
        self.nodes.append((ID,ToGP2Helper(label),info))

    def addEdge(self,ID,edgeFrom,edgeTo,label="empty"):
        """Add an edge to the graph

        Args:
            ID (int): Index of the edge
            edgeFrom (int): Source of the edge
            edgeTo (int): Target of the edge
            label (str, optional): Order of the child node. Defaults to "empty".
        """
        self.edges.append((ID,edgeFrom,edgeTo,label))

    
def ToGP2Helper(label):
    '''
    Covert Essence string to GP2-safe string.
    '''
    if label == '/\\':
        return "AND"
    if label == '\\/':
        return "OR"
    if label == '!':
        return "NOT"
    if label == '->':
        return "IMPLY"
    if label == '>':
        return "GREATER"
    if label == '<':
        return "SMALLER"
    if label == '>=':
        return "GREATERTN"
    if label == '<=':
        return "SMALLERTN"
    
    return label

def ToEssenceHelper(label_full):
    '''
    Convert to GP2-safe string back to Essence. Use inside any converter that leads to Essence
    '''
    parts = label_full.split(" # ")
    gp2_label = parts[0]
    label = ''
    flag = ""
    if len(parts) >1:
        flag = "# " + parts[1]
    if gp2_label == "AND": label = "/\\"
    elif gp2_label == "OR": label = "\\/"
    elif gp2_label == "NOT": label = "!"
    elif gp2_label == "IMPLY": label = '->'
    elif gp2_label == "GREATER": label = '>'
    elif gp2_label == "SMALLER": label = '<'
    elif gp2_label == "GREATERTN": label = '>='
    elif gp2_label == "SMALLERTN": label = '<='
    else: label = gp2_label

    return label+flag

