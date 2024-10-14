'''
Methods to transform an AST into normal form; currently quite limited.
'''
import functools

normalisable = ["RelationConstant", "BinaryExpression", "root"]
statementsOrder = {"NameLettingStatement": 1, 
                   "DomainNameLettingStatement" :2,
                   "FindStatement" : 3,
                   "SuchThatStatement" : 4}
# Order literals < ops < digits
binaryOpNormalisable = ["*","+","=", "!=", "/\\","\\/"]

def normaliseASTpy(node):
    '''
    Put AST in normal form (preliminary code).
    Currently only sorts children, aim is to extend this to full normal form.
    '''
    if node.info in normalisable:
        node.children = reOrder(node)
    for child in node.children:
        normaliseASTpy(child)


def reOrder(node):
    '''
    Sort children of node.
    Currently applied to binary expressions and to group together
    letting/find/such that statements.
    '''
    if node.info == "RelationConstant":
        print("what to do with the tuples ?")
    elif node.info == "BinaryExpression":
        if node.label in binaryOpNormalisable:
            node.children = sorted(node.children,  key=lambda x: x.label)
    elif node.info.lower() == "root":
        node.children = sorted(node.children, key=functools.cmp_to_key(compareStatements))
    return node.children

def compareStatements(x,y):
    '''
    Classify statements by general category.
    '''
    return statementsOrder[x] - statementsOrder[y]

def compareExpression(exp1, exp2):
    '''
    currently just a placeholder
    '''
    return 0
