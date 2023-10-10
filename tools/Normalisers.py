import functools

normalisable = ["RelationConstant", "BinaryExpression", "root"]
statementsOrder = {"NameLettingStatement": 1, 
                   "DomainNameLettingStatement" :2,
                   "FindStatement" : 3,
                   "SuchThatStatement" : 4}
# Order Chars <symbols< numbers
binaryOpNormalisable = ["*","+","=", "!=", "/\\","\\/"]

def normaliseASTpy(node):
    if len(node.Children) >= 2:
        if node.info in normalisable:
            node.children = reOrder(node)


def reOrder(node):
    if node.info == "RelationConstant":
        print("what to do with the tuple children as they are indistinguishable")
    elif node.info == "BinaryExpression":
        if node.label in binaryOpNormalisable:
            node.children = sorted(node.children,  key=lambda x: x.label)
    elif node.info.lower() == "root":
        node.children = sorted(node.children, key=functools.cmp_to_key(compareStatements))
    return node.children

def compareStatements(x,y):
    return statementsOrder[x] - statementsOrder[y]
