import re

class Graph:
    def __init__(self, nodes = [], edges =[]):
        self.nodes = nodes
        self.edges = edges

    def addNode(self, ID,label="empty",info = ""):
        self.nodes.append((ID,ToGP2Helper(label),info))

    def addEdge(self,ID,edgeFrom,edgeTo,label="empty"):
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

def ToEssenceHelper(label):
    '''
    Convert to GP2-safe string back to Essence. Use inside any converter that leads to Essence
    '''
    if label == "AND":
        return "/\\"
    if label == "OR":
        return "\\/"
    if label == "NOT":
        return "!"
    if label == "IMPLY":
        return '->'
    if label == "GREATER":
        return '>'
    if label == "SMALLER":
        return '<'
    if label == "GREATERTN":
        return '>='
    if label == "SMALLERTN":
        return '<='

    return label

