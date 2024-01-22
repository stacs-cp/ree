import eminipyparser as ep
import networkx as nx

def specToInstaGen(AST):
    '''
    From Emini AST spec to Instance Generator

    TODO: improve this eye sore
    '''
    parameters ={}
    # remove find and such that statements
    AST.children = [child for child in AST.children if not(isinstance(child, ep.FindStatement) or isinstance(child, ep.SuchThatStatement))]
    #AST.children = [givenIntTOfindInt(child) for child in AST.children if (isinstance(child, ep.GivenStatement) and isinstance(child.children[0], ep.IntDomain))]
    for i,child in enumerate(AST.children):
        if child.children[0].children[0].info == "IntDomain":
            bounds = []
            if child.children[0].children[0].children[0].label.isdigit():
                bounds.append(child.children[0].children[0].children[0].label)
            elif child.children[0].children[0].children[0].info == "ReferenceToParameter":
                bounds.append(parameters[child.children[0].children[0].children[0].label][0])
            else:
                print("Warning: bound retrival error")
                print(child.children[0].children[0].children[0].info)
            if child.children[0].children[0].children[1].label.isdigit():
                bounds.append(child.children[0].children[0].children[1].label)
            elif child.children[0].children[0].children[1].info == "ReferenceToParameter":
                bounds.append(parameters[child.children[0].children[0].children[1].label][1])
            else:
                print("Warning: bound retrival error")
                print(child.children[0].children[0].children[1].info)
            if child.children[0].info == "Parameter": 
                parameters[child.children[0].label] = bounds
            child.children[0].children[0] = ep.IntDomain(ep.IntConstant(bounds[0]),ep.IntConstant(bounds[1]))
        if isinstance(child, ep.GivenStatement):            
            AST.children[i] = givenTOfind(child)
        if isinstance(child, ep.WhereStatement):
            AST.children[i] = whereTOsuchthat(child)
    print(parameters)
    return AST

def givenTOfind(statement):
    ''' Turn a GIVEN statement into a FIND statement
    '''
    return ep.FindStatement(statement.children[0].label,statement.children[0].children[0])

def whereTOsuchthat(statement):
    ''' turn a WHERE statement into a SUCH THAT statement
    '''
    return ep.SuchThatStatement(statement.children)

def NXtoEssenceRelation(NXgraph, vertices_name="vertices", relation_name = "edges"):
    '''
    From networkx graph to Emini relation
    '''
    # TODO store vertices labels somewhere
    edges = ""
    for e in nx.generate_edgelist(NXgraph, data=False):
        edges += f'({e[0]},{e[2]})'
    return f'''letting {vertices_name} be domain int(0..{len(NXgraph.nodes())-1})
letting {relation_name} be relation({edges})'''

def injectGraphByName(AST, vertices_name, relation_name, verticesAST,graphAST):
    for i,child in enumerate(AST.children):
        if isinstance(child, ep.NameLettingStatement):
            if child.children[0].label == vertices_name:
                AST.children[i] = verticesAST
            if child.children[0].label == relation_name:
                AST.children[i] = graphAST
            




    