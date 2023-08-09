binary_operators = ["<",">", "<=", ">=", "+", "-", "*", "/", "%", "=","!=", "->", "/\\", "xor","\\/" , "and" , "in"]

def ASTtoEssence(AST):
    '''
    Turns an Abstract Syntax Tree of python objects into an Essence-Mini specification (string) 
    '''
    spec = ""
    for statement in AST.children:
        spec += iceStatement(statement)
        spec += "\n"
    return spec

def iceStatement(node):
    if node.info == 'GivenStatement':
        return iceGivenParameter(node)
    if node.info == "WhereStatement":
        return iceWhere(node)
    if node.info == "NameLettingStatement":
        return iceLettingConstant(node)
    if node.info == "DomainNameLettingStatement":
        return iceLettingDomain(node)
    if node.info == "FindStatement":
        return iceFind(node)
    if node.info == "SuchThatStatement":
        return iceSuchThat(node)
    

def iceGivenParameter(node):
    statement = "given "
    statement += node.children[0].label # The first child of a given statement is always the name
    statement += " : " 
    statement += iceDomain(node.children[0].children[0]) # the first grandchild is the domain 
    return statement

def iceWhere(node):
    statement = "where \n  "
    constraints = []
    for expression in node.children: # get all stacks for all comma separated expressions
        iceConstraints(expression,constraints)
        constraints.append("\n  ,\n  ")
    constraints = "".join(constraints[:-1]) # merge the constraints in each stack
    statement += constraints
    return statement

def iceLettingConstant(node):
    statement = "letting "
    statement += node.children[0].label # The first child of a letting statement is always the name
    statement += " be " 
    statement += iceConstants(node.children[0].children[0]) # the first grandchild is the value 
    return statement

def iceLettingDomain(node):
    statement = "letting "
    statement += node.children[0].label # The first child of a letting statement is always the name
    statement += " be domain " 
    statement += iceDomain(node.children[0].children[0]) # the first grandchild is the domain 
    return statement

def iceFind(node):
    statement = "find "
    statement += node.children[0].label # The first child of a find statement is always the name
    statement += " : " 
    statement += iceDomain(node.children[0].children[0]) # the first grandchild is the domain 
    return statement

def iceSuchThat(node):
    statement = "such that \n  "
    constraints = []
    for expression in node.children: # get all stacks for all comma separated expressions
        iceConstraints(expression,constraints)
        constraints.append("\n  ,\n  ")
    constraints = "".join(constraints[:-1]) # merge the constraints in each stack
    statement += constraints
    return statement

def iceConstraints(node, constraints):
    if node.label == " . " or node.label == ". " or node.label == ".":
        iceConstraints(node.children[0], constraints)
        constraints.append(" . " + "\n  ")   ## BUG potential issues here
        iceConstraints(node.children[1], constraints)
    elif node.info == "QuantificationExpression":
        constraints.append(iceQuantifier(node))
    else:
        constraints.append(iceExpression(node))      

def iceConstants(node):
    if node.info == "Integer" or node.info == "Literal":
        return node.label
    elif node.label == "relation":
        relation = node.label
        relation += "("
        for tuple in node.children:
            relation += "("
            relation += ",".join(t.label for t in tuple.children)
            relation += ")"
        relation += ")"
        return relation
    elif node.label == "tuple":
        tuple = ""        
        tuple += "("
        tuple += ",".join(t.label for t in node.children)
        tuple += ")"
        return tuple
    else:
        raise Exception("Something went wrong when icing Constant:" + node.label)
    
def iceExpression(node):
    expression = ""
    stack = []
    expressionInOrderTraversal(node,stack,None)
    expression = " ".join(stack)
    return expression

def iceQuantifier(node):
    quantifier = node.label + " "
    quantifier += iceLocalVariables(node.children[:-1]) + " "
    quantifier += node.children[-1].label + " " # preposition
    quantifier += node.children[-1].children[0].label # set or expression TODO fix
    return quantifier

def iceLocalVariables(variables):
    localVariables = ""
    if type(variables) == list:
        vars = []
        for var in variables:            
            vars.append(iceLocalVariables(var))
        localVariables += ",".join(vars)
    elif variables.info == "TupleVariable":
        localVariables += "("
        localVariables += ",".join(v.label for v in variables.children)
        localVariables += ")"
    else:
        localVariables += variables.label
    return localVariables

def expressionInOrderTraversal(node, stack, parent):   
    parentheses = needsParenethesis(node,parent)

    if len(node.children) == 2 and node.label in binary_operators:  # check if it is binary subtree
        if parentheses: stack.append("(") # left parenthesis if needed
        expressionInOrderTraversal(node.children[0], stack, node) # left
        stack.append(node.label) #op
        expressionInOrderTraversal(node.children[1], stack, node) # right
        if parentheses: stack.append(")") # right parenthesis if needed

    elif len(node.children) == 1 and node.info != "MemberExpression": # check if it has at least one child (for unary)
        if parentheses: stack.append("(")          
        stack.append(node.label)
        expressionInOrderTraversal(node.children[0], stack, node)
        if parentheses: stack.append(")") 
    elif node.info == "MemberExpression":
        stack.append(iceMemberExpression(node))   
    elif node.label == "tuple":
        stack.append(iceConstants(node))
    else:
        stack.append(node.label)

def iceMemberExpression(node):
    memberExpression = ""
    memberExpression += node.label
    if node.children[0].label == "tuple":
        memberExpression += "("
        memberExpression += ",".join(v.label for v in node.children[0].children)
        memberExpression += ")"
    elif len(node.children) == 1:
        memberExpression += "["
        memberExpression += node.children[0].label
        memberExpression += "] "
    else:
        raise Exception("Something went wrong when icing MemberExpression:" + node.label)
    return memberExpression


def needsParenethesis(node,parent):
    if parent != None:
        return precedence(node.label) < precedence(parent.label)
    else:
        return False
    
def precedence(op):
            if op == "->":
                return -4
            if op == "/\\":
                return -1
            if op == "xor":
                return -2
            if op == "\\/":
                return -3
            if op in ["<", ">", "<=", ">=","=", "!="]:
                return 0
            if op == "in":
                return 0
            if op in ["+", "-"]:
                return 1
            if op in ["*", "/"]:
                return 3
            if op in ["u-", "u!"]:   ## UNARY OPERATORS
                return 8
            if op == "(":
                return 9
            return 999
    

def iceDomain(node):
    domain = ""
    if node.info == "IntDomain":
        domain += "int("
        domain += iceExpression(node.children[0]) #lower bound
        domain += ".."
        domain += iceExpression(node.children[1]) # upper bound
        domain += ")"
    if node.info == "RelationDomain":
        domain += "relation"
        domainsStart = 0
        if node.children[0].label in ["size", "minSize","maxSize"]: # bounded relation keep the size inthe first child
            domain += " ("
            domain += f'{node.children[0].label} ' 
            domain += iceExpression(node.children[0].children[0]) # first grandchild is the value
            domain += ") "
            domainsStart = 1
        domains = [iceDomain(d) for d in node.children[domainsStart:]]
        domain += " of (" + "*".join(domains)+")"   
    if node.info == "TupleDomain":
        domain += "tuple"
        domains = [iceDomain(d) for d in node.children]
        domain += "(" + ",".join(domains) +")"

    if node.info == "BoolDomain":
        domain += "bool"
    
    if node.info == "ReferenceToNamedDomain":
        domain += node.label # first child is the reference
    
    if domain == "":
        print("domain gone wrong")

    return domain
