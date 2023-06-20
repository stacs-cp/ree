import re
import networkx as nx
import copy

class Node:
    def __init__(self, label, children=[],info = ""):
        self.label = label
        self.children = children
        if info == "":
            self.info = str(type(self)).split('.')[-1][:-2] 
        else:
            self.info = info

### Statements
class NameLettingStatement(Node):
    def __init__(self, name, constant):
        super().__init__("letting", [Node(name,[constant])])

class DomainNameLettingStatement(Node):
    def __init__(self, name, domain):
        super().__init__("letting", [Node(name,[domain])])

class FindStatement(Node):
    def __init__(self, name, domain):
        super().__init__("find", [Node(name,[domain], "DecisionVariable")])
    
class SuchThatStatement(Node):
    def __init__(self, constraints):
        super().__init__("such that", constraints)
    
### Domains
class IntDomain(Node):
    def __init__(self, lower,upper):
        super().__init__("int", [lower,upper])
    
class TupleDomain(Node):
    def __init__(self, domains):
        super().__init__("tuple", domains)
    
class RelationDomain(Node):
    def __init__(self, domains):
        super().__init__("relation", domains)

class BoolDomain(Node):
    def __init__(self):
        super().__init__("bool")
    
### Constants
class IntConstant(Node):
    def __init__(self, label):
        super().__init__(label)
    
class TupleConstant(Node):
    def __init__(self, values):
        super().__init__("tuple", values)
    
class RelationConstant(Node):
    def __init__(self, values):
        super().__init__("relation", values)

class BoolConstant(Node):
    def __init__(self, label):
         super().__init__(label)
    
##### Expressions
class Expression(Node):
    def __init__(self, label, children = []):
        super().__init__(label, children)

class QuantificationExpression(Node):
    def __init__(self, quantifier, variables, preposition, domain):
        super().__init__(quantifier, [*variables, Node(preposition,[domain], "Preposition")]) ## require ad hoc normalisation rule for variables that exclude last element of list (preposition)

class UnaryExpression(Node):
    def __init__(self, label, child):
        super().__init__(label, [child])

class BinaryExpression(Node):
    def __init__(self, label, left,right):
        super().__init__(label, [left,right]) ## normalisation operator dependant 

class MemberExpression(Node):
    def __init__(self, identifier, elements):
        super().__init__(identifier, elements)

# reserved words find, such, given, forAll, exists, 
class EssenceParser:
    def __init__(self):
        self.tokens = []
        self.index = 0
        self.named_domains = {} 
        self.named_constants = {}
        self.decision_variables = {}
        self.binary_operators = ["<",">", "<=", ">=", "+", "-", "*", "/", "%", "=","!=", "->", "/\\", "xor","\\/" , "and" , "in"]
        self.unary_operators = ["u-","!"]
        self.statements = []

    def removeComments(self, spec):
        lines = spec.split('\n')
        newSpec = ""
        for line in lines:
            newSpec += line.split('$',1)[0] + " "
        return newSpec
    
    def parse(self, essenceSpec):
        commentlessStr = self.removeComments(essenceSpec)
        commentlessStr = commentlessStr.replace(r'/\\n', '/\\')
        self.tokens = re.findall(r'\.\.|\->|\\/|/\\|>|<|>=|<=|!=|!|==|=|\+|[^=!<>+\s\w]|[\w]+', commentlessStr.replace('\n', ' '))

        #print(' '.join(self.tokens))
        while self.index < len(self.tokens):
            statement = self.parse_statement()
            if statement.info == "NameLettingStatement":
                self.named_constants[statement.label] = statement.children[0]
            if statement.info == "DomainNameLettingStatement":
                self.named_domains[statement.children[0].label] = statement.children[0]
            if statement.info == "FindStatement":    
                self.decision_variables[statement.children[0].label] = statement.children[0]                
            self.statements.append(statement)
        if self.index < len(self.tokens):
            raise Exception("Something went wrong. Parsed until: " + str(self.tokens[self.index]) + " at Token Num: " + str(self.index))
        return self.statements

    def consume(self):
        token = self.tokens[self.index]
        self.index += 1
        return token

    def match(self, expected):
        return self.index < len(self.tokens) and self.tokens[self.index] == expected
    
    def match_any(self, tokens):
        return any(self.match(token) for token in tokens)

    def parse_statement(self):
        if self.match("letting"):          
          if self.tokens[self.index + 2] == "be" and self.tokens[self.index + 3] == "domain":
            return self.parse_domain_name_letting_statement()
          if self.tokens[self.index + 2] == "be":
            return self.parse_name_letting_statement()
          else:
              raise SyntaxError("Invalid letting statement: " + str(self.tokens[self.index]))
        elif self.match("find"):
            return self.parse_find_statement()
        elif self.match("such"):
            return self.parse_such_that_statement()
        else:
            raise SyntaxError("Invalid statement:" +str( self.tokens[self.index]) + " Token Num: " + str(self.index))

    def parse_name_letting_statement(self):
        self.consume()  # "letting"
        name = self.consume()  # Name
        self.consume()  # "be"
        constant = self.parse_constant()
        return NameLettingStatement(name, constant)

    def parse_domain_name_letting_statement(self):
        self.consume()  # "letting"
        name_of_domain = self.consume()  # NameDomain
        self.consume()  # "be "
        self.consume()  # "domain"
        domain = self.parse_domain()
        return DomainNameLettingStatement(name_of_domain, domain)

    def parse_find_statement(self):
        self.consume()  # "find"
        name = self.consume()  # Name
        column = self.consume()
        if column != ":":
            raise SyntaxError("Invalid Token - Expected : instead of " + column + " Token Num: " + str(self.index-1))
        domain = self.parse_domain()    
        return FindStatement(name, domain)   

    def parse_such_that_statement(self):
        such_that_list = []
        self.consume()  # "such"
        that = self.consume()
        if that != "that": # "that"
            raise SyntaxError("Expected \"that\" but got: " + that + " .Token Num: " + str(self.index-1))
        expression = self.parse_expression()

        while self.match_any([".", ',']):
            matched = self.consume()  # "."
            if matched == "." :
                next_expression = self.parse_expression()
                expression = Node(" . ", [expression, next_expression], "ConcatenationExpression")
            else: ## something not working here. maybe
                such_that_list.append(expression)
                expression = self.parse_expression()

        such_that_list.append(expression)
        return SuchThatStatement(such_that_list)


    def parse_domain(self):
        if self.match("int"):
            self.consume()  # "int"
            self.consume()  # "("
            lower = self.parse_expression()  # Lower bound
            self.consume()  # ".."
            upper = self.parse_expression()  # Upper bound
            return IntDomain(lower,upper)            
        elif self.match("tuple"):
            self.consume()  # "tuple"
            self.consume()  # "("
            domains = []
            while not self.match(")"):
                domains.append(self.parse_domain())
                if self.match(","):
                    self.consume()  # ","
            self.consume()  # ")"
            return TupleDomain(domains)

        elif self.match("relation"):
            domains = []
            self.consume()  # "relation"
            if self.match("("):
                self.consume() # (
                if self.match_any(["size", "minSize","maxSize"]):
                    boundKind = self.consume() # size
                    size = self.parse_expression() #
                    domains.append(Node(boundKind, [size], "RelationSize"))
                else:
                    SyntaxError("Relation Size Parsing Error. Expected size instead of Token: " + str(self.tokens[self.index]))
            self.consume()  # "of"
            self.consume()  # "("               
            while not self.match(")"):
                domains.append(self.parse_domain())
                if self.match("*"):
                    self.consume()  # "*"
            self.consume()  # ")"
            return RelationDomain(domains)
        elif self.match("bool"):
            self.consume()  # "bool"            
            return BoolDomain()
        elif self.tokens[self.index] in self.named_domains:
            name_of_domain = self.consume()
            #return NamedDomain(name_of_domain,self.named_domains[name_of_domain].domain) ## TEST
            return Node(name_of_domain, info="ReferenceToNamedDomain")
        else:
            raise SyntaxError("Domain Parsing Error. Token: " + str(self.tokens[self.index]))    

    def parse_constant(self):
        # tuple - relation - int 
        if self.match("(") and self.tokens[self.index + 2] == ",":
            return self.parse_tuple_constant()        
        elif self.match("relation"):
            return self.parse_relation_constant()
        elif self.tokens[self.index].isdigit():
            return Node(self.consume(),info = "Integer") ## should it be parse_expression?
        elif self.index + 2 < len(self.tokens):
            if self.match("(") and self.tokens[self.index + 2] == ")":
                return self.parse_tuple_constant()
            else:
                raise SyntaxError("Invalid constant: " + str(self.tokens[self.index]))
        else:
            raise SyntaxError("Invalid constant: " + str(self.tokens[self.index]))

    def parse_literal(self):
        # single integer
        if self.tokens[self.index].isdigit():
            return Node(self.consume(),info = "Integer")
        elif self.match("(") and self.tokens[self.index + 2] == ",":            
            return self.parse_tuple_constant()
        else: 
            identifier = self.consume()
            if self.index +2 < len(self.tokens): 
                if self.tokens[self.index] == '[' and self.tokens[self.index +2] == ']': ## element of tuple i.e. a[1]
                    self.consume() # [
                    element = self.parse_literal()
                    self.consume() # ]
                    return MemberExpression(identifier, [element])
                ### TODO generalise to relation of any arity
                if self.tokens[self.index] == '(' and self.tokens[self.index +2] == ')': ## element of relation i.e. a(b,c)
                    self.consume()  # "("
                    tuple_elements = []
                    while not self.match(")"):
                        tuple_elements.append(Node(self.consume(), info="Literal"))
                        if self.match(","):
                            self.consume()  # ","
                    self.consume()  # ")"
                    return MemberExpression(identifier, tuple_elements)
            if self.match("(") and self.tokens[self.index + 2] == ",":
                return MemberExpression(identifier, [self.parse_tuple_constant()]) 
            if identifier in self.decision_variables:
                return Node(identifier, info="ReferenceToDecisionVariable")
            if identifier in self.named_domains:
                return Node(identifier, info="ReferenceToNamedDomain")
            if identifier in self.named_constants:
                return Node(identifier, info="ReferenceToNamedContanst")
            return Node(identifier, info="Literal")

    def is_expression_terminator(self):
        return (
            self.match(".")
            or self.match(",")
            or self.match("such")
            or self.match("letting")
            or self.match("find")
            or self.match("..")
            or self.match("of")
            or self.index >= len(self.tokens)
        )    
    
    def parse_expression(self):
        ## Quantification
        if self.match_any(["forAll", "exists"]):
             return self.parse_quantification()

        ## TODO separate quantifier and arithmetic expressions 
        ## Expression with Parentheses
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
            
            print("missing operator")
            return 999

        output_queue = []
        operator_stack = []

        while not self.is_expression_terminator():
            if self.match("(") and self.tokens[self.index + 2] != ",":
                operator_stack.append(Node(self.consume(),info="Parenthesis"))  # "("
            elif self.match(")"):
                while operator_stack and operator_stack[-1].label != "(":
                    output_queue.append(operator_stack.pop())
                if operator_stack:
                    operator_stack.pop()  # remove the "("
                self.consume()  # ")"
            elif self.checkUnaryOperator(output_queue):
                uOperator = 'u'+self.consume()
                current_operator = Node(uOperator,info="UnaryOperator")
                while (operator_stack and operator_stack[-1].label != "("
                        and precedence(operator_stack[-1].label) > precedence(current_operator.label)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(current_operator)
            elif self.match_any(self.binary_operators):
                current_operator = Node(self.consume(),info="BinaryOperator")
                while (operator_stack and operator_stack[-1].label != "("
                        and precedence(operator_stack[-1].label) >= precedence(current_operator.label)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(current_operator)
            else:
                output_queue.append(self.parse_literal())  # Literal or Name
            

        while operator_stack:
            output_queue.append(operator_stack.pop())
        return self.build_expression_tree(output_queue)

    def build_expression_tree(self, postfix_expression):
        stack = []
        for token in postfix_expression:            
            if token.info == "UnaryOperator":
                right = stack.pop()              
                stack.append(UnaryExpression(token.label[-1], right))
            elif token.info == "BinaryOperator":
                right = stack.pop()
                left = stack.pop()
                stack.append(BinaryExpression(token.label, left,right))
            elif isinstance(token, Node):
                stack.append(token)
            else:
                stack.append(Node(token))
                print("something not right at " + token + " Token Num: " + str(self.index))
        return stack[0]    

    def checkUnaryOperator(self,output_queue):
        if self.match("-"):
            if self.index>0 and self.tokens[self.index-1] in self.binary_operators:
                return True
            elif len(output_queue) ==0:
                return True
            elif self.tokens[self.index+1]== "(":
                return True
            else:
                return False
        elif self.match("!"):
            return True
        else:
            return False
        
    def parse_tuple_constant(self):
        self.consume()  # "("
        values = []
        while not self.match(")"):
            values.append(Node(self.consume(), info="Literal"))  # Literal 
            if self.match(","):
                self.consume()  # ","
        self.consume()  # ")"
        return TupleConstant(values)

    def parse_relation_constant(self):
        self.consume()  # "relation"
        self.consume()  # "("
        values = []
        while not self.match(")"):
            if self.match("("):
                values.append(self.parse_tuple_constant())
            if self.match(","):
                self.consume()  # ","
        self.consume()  # ")"
        return RelationConstant(values)

    def parse_quantification(self):
        quantifier = self.consume()  # "forAll" or "exists"
        variables = []

        while not self.match_any([":", "in"]):
            if self.match("("):
                self.consume()  # "("
                tuple_elements = []
                while not self.match(")"):
                    tuple_elements.append(Node(self.consume(), info="LocalVariable"))
                    if self.match(","):
                        self.consume()  # ","
                self.consume()  # ")"
                variables.append(Node("Tuple", tuple_elements,"TupleVariable"))
            else:
                variables.append(Node(self.consume(), info="LocalVariable"))
                if self.match(","):
                    self.consume()  # ","

        preposition = self.consume()  # ":" or "in"
        if preposition == ":":
           domain = self.parse_domain()
        else:
           domain = self.parse_literal() ## NEEDS REVISION
        return QuantificationExpression(quantifier,variables, preposition,domain)
 

def buildTreeNX(node, Tree, nodeIndex=None, parent=None):                
    Tree.add_node(id(node), value = node.label, index = nodeIndex) 
    if parent != None: 
        Tree.add_edge(id(parent), id(node))
    for i in range(len(node.children)):
        buildTreeNX(node.children[i], Tree, i+1, node)

def getNXTree(title = None, statements = []):
    '''
    Returns a nx tree graph from a list of statements
    '''
    G = nx.DiGraph()
    buildTreeNX(Node(title, statements), G)
    return G

def printTree(node, indent="", last = True, printInfo = False):
    '''
    Draw the provided tree as console text recursively from a starting node
    '''
    info = ""
    if printInfo:
        info = "  #"+ node.info    
    branch = ""
    extension = ""
    if last:
        branch = "┕"
        extension = "   "
    else:
        branch = "┝"
        extension = "|  "
    print(indent + branch+"- " + node.label +info)
    indent += extension
    for i in range(len(node.children)):
        printTree(node.children[i], indent, i==len(node.children)-1,printInfo=printInfo)

def treeEquality(subTree1, subTree2): 
  '''
  Tests if 2 trees are identical all the way down.
  '''               
  if subTree1.label != subTree2.label:
      return False
  
  if len(subTree1.children) != len(subTree2.children):
      return False
  elif len(subTree1.children) > 0 and len(subTree2.children) > 0:
    isEqual = True
    for i in range(len(subTree1.children)):
      isEqual = isEqual and treeEquality(subTree1.children[i],subTree1.children[i])
    return isEqual
  elif len(subTree1.children) == 0 and len(subTree2.children) == 0:
      return True