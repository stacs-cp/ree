'''
add back syntactic sugar elided in internal AST representation (not comments)
'''

binary_operators = [".","<",">", "<=", ">=", "+", "-", "*", "/", "%", "=","!=", "->", "/\\", "xor","\\/" , "and" , "in", "subset","subsetEq","intersect","union"]

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
    '''
    deal with each type of statement
    '''
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
    '''
    given statement
    '''
    statement = "given "
    statement += node.children[0].label # Name. The first child of a given statement is always the name
    statement += " : " 
    statement += iceDomain(node.children[0].children[0]) # the first grandchild is the domain 
    return statement

def iceWhere(node):
    '''
    where statement
    '''
    statement = "where \n  "
    constraints = []
    for expression in node.children: # get all stacks for all comma separated expressions
        iceConstraints(expression,constraints)
        constraints.append("\n  ,\n  ")
    constraints = "".join(constraints[:-1]) # merge the constraints in each stack
    statement += constraints
    return statement

def iceLettingConstant(node):
    '''
    letting statement, constant
    '''
    statement = "letting "
    statement += node.children[0].label # The first child of a letting statement is always the name
    statement += " be " 
    statement += iceConstants(node.children[0].children[0]) # the first grandchild is the value 
    return statement

def iceLettingDomain(node):
    '''
    letting statement, domain
    '''
    statement = "letting "
    statement += node.children[0].label # The first child of a letting statement is always the name
    statement += " be domain " 
    statement += iceDomain(node.children[0].children[0]) # the first grandchild is the domain 
    return statement

def iceFind(node):
    '''
    find statement
    '''
    statement = "find "
    statement += node.children[0].label # The first child of a find statement is always the name
    statement += " : " 
    statement += iceDomain(node.children[0].children[0]) # the first grandchild is the domain 
    return statement

def iceSuchThat(node):
    '''
    such that statement
    '''
    statement = "such that\n"
    constraints = []
    for expression in node.children: # get all stacks for all comma separated expressions
        iceConstraints(expression,constraints)
        constraints.append("\n   ,\n")
    constraints = "".join(constraints[:-1]) # merge the constraints in each stack
    statement += constraints
    return statement

def iceConstraints(node, constraints, spacer=""):
    '''
    constraints
    '''
    
    constraints.append(spacer)
    spacer += " " 
    if node.label == " . " or node.label == ". " or node.label == ".":
        iceConstraints(node.children[0], constraints,spacer)
        constraints.append(" .\n")   ## BUG potential issues here
        spacer += " "
        iceConstraints(node.children[1], constraints,spacer)
    elif node.info == "QuantificationExpression":
        constraints.append(iceQuantifier(node))
    else:
        constraints.append(spacer)
        constraints.append(iceExpression(node)) 
       

def iceConstants(node):
    '''
    constants
    '''
    if node.info in ["Integer", "Literal", "Boolean", "ReferenceToNamedConstant","ReferenceToParameter","ReferenceToDecisionVariable"]:
        return node.label
    elif node.label == "relation":
        relation = node.label
        relation += "("
        for tuple in node.children:
            relation += "("
            relation += ",".join(iceConstants(item) for item in node.children)
            relation += ")"
        relation += ")"
        return relation
    elif node.label == "set":
        set_constant = ""        
        set_constant += "{"
        set_constant += ",".join(iceConstants(item) for item in node.children)
        set_constant += "}"
        return set_constant
    elif node.label == "function":
        function_constant = node.label
        function_constant += "("
        function_constant += ",".join(iceConstants(item) for item in node.children)
        function_constant += ")"
        return function_constant
    elif node.label == "functionItem":
        function_item = iceConstants(node.children[0])
        function_item += " --> " 
        function_item += iceConstants(node.children[1])
        return function_item
    elif node.label == "tuple":
        tuple = ""        
        tuple += "("
        tuple += ",".join(iceExpression(item) for item in node.children)
        tuple += ")"
        return tuple
    else:
        print(node.children[0].label)
        raise Exception(f"Something went wrong when icing Constant: {node.label} Info:{node.info}")
    
def iceExpression(node):
    '''
    expression
    '''
    expression = ""
    stack = []
    expressionInOrderTraversal(node,stack,None)
    expression = " ".join(stack)
    return expression

def iceQuantifier(node):
    '''
    quantifier
    '''
    quantifier = node.label + " "
    quantifier += iceLocalVariables(node.children[:-1]) + " "
    quantifier += node.children[-1].label + " " # preposition
    if node.children[-1].label == ":":
        quantifier += iceDomain(node.children[-1].children[0])
    else:
        quantifier += node.children[-1].children[0].label # set or expression TODO fix
    return quantifier

def iceLocalVariables(variables):
    '''
    local variables
    '''
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
    '''
    expression, respecting ordered children
    '''
    parentheses = needsParenthesis(node,parent)

    if len(node.children) == 2 and node.label in binary_operators:  # check if it is binary subtree
        if parentheses: stack.append("(") # left parenthesis if needed
        expressionInOrderTraversal(node.children[0], stack, node) # left
        stack.append(node.label) #op
        expressionInOrderTraversal(node.children[1], stack, node) # right
        if parentheses: stack.append(")") # right parenthesis if needed

    elif len(node.children) == 1 and node.info != "MemberExpression" and node.info != 'SetConstant': # check if it has at least one child (for unary)
        if parentheses: stack.append("(")          
        stack.append(node.label)
        expressionInOrderTraversal(node.children[0], stack, node)
        if parentheses: stack.append(")") 
    elif node.label == "toInt":        
        stack.append(node.label)
        stack.append("(")
        expressionInOrderTraversal(node.children[0], stack, node)
        stack.append(")") 
    elif node.info == "MemberExpression":
        stack.append(iceMemberExpression(node))   
    elif node.label in ["tuple"]:
        stack.append(iceConstants(node))
    elif node.info == "QuantificationExpression":
        stack.append(iceQuantifier(node))
    elif node.info == 'SetConstant':
        stack.append(iceConstants(node))
    else:
        stack.append(node.label)

def iceMemberExpression(node):
    '''
    member expression
    '''
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


def needsParenthesis(node,parent):
    '''
    put back parenthesis if it is needed to maintain semantics
    '''
    if parent != None and parent.label != "->":
        return precedence(node.label) < precedence(parent.label)
    elif parent != None and parent.label == "->":
        if parent.children[1].label == "->":
            return True
        else:
            return False
    else:
        return False
    
def precedence(op):
    '''
    compute operator precedence
    should this be merged with eminipyparser.precedence()?
    '''
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
    if op in ["subset","subsetEq"]:
        return 1
    if op in ["intersect", "union"]:
        return 2
    if op in ["+", "-"]:
        return 3
    if op in ["*", "/","%"]:
        return 4
    if op in ["u-", "u!"]:   ## UNARY OPERATORS
        return 8
    if op == ".":
        return -11
    if op == "(":
        return 9
    return 999
    

def iceDomain(node):
    '''
    domains
    '''
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
        for child in node.children:            
            if child.info== "Attribute":
                if domainsStart == 0:
                    domain += " ("
                if domainsStart >0:
                    domain += ", "
                if child.label in ["size", "minSize","maxSize"]: # bounded relation keep the size inthe first child                    
                    domain += f'{child.label} ' 
                    domain += iceExpression(child.children[0]) # first grandchild is the value                    
                else:
                    domain += f'{child.label} ' 
                domainsStart += 1
        if domainsStart >0:
            domain += ")"
        domains = [iceDomain(d) for d in node.children[domainsStart:]]
        domain += " of (" + "*".join(domains)+")"         
    if node.info == "SetDomain":
        domain += "set"
        domainsStart = 0
        for child in node.children:            
            if child.info== "Attribute":
                if domainsStart == 0:
                    domain += " ("
                if domainsStart >0:
                    domain += ", "
                if child.label in ["size", "minSize","maxSize"]: # bounded relation keep the size inthe first child                    
                    domain += f'{child.label} ' 
                    domain += iceExpression(child.children[0]) # first grandchild is the value                    
                else:
                    domain += f'{child.label} ' 
                domainsStart += 1
        if domainsStart >0:
            domain += ")"
        domain += " of "
        domain += iceDomain(node.children[-1])

    if node.info == "FunctionDomain":
        domain += "function"
        domainsStart = 0
        for child in node.children:            
            if child.info== "Attribute":
                if domainsStart == 0:
                    domain += " ("
                if domainsStart >0:
                    domain += ", "
                if child.label in ["size", "minSize","maxSize"]: # bounded relation keep the size inthe first child                    
                    domain += f'{child.label} ' 
                    domain += iceExpression(child.children[0]) # first grandchild is the value                    
                else:
                    domain += f'{child.label}' 
                domainsStart += 1
        if domainsStart >0:
            domain += ") "
        # Last 2 elements of the array are always the domain and codomain of the function
        domain += iceDomain(node.children[-2])
        domain += " --> "  
        domain += iceDomain(node.children[-1])

     
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
