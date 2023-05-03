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
    def __init__(self, name, value):
        super().__init__("letting", [Node(name,[value])])

class DomainNameLettingStatement(Node):
    def __init__(self, name, domain):
        super().__init__("letting", [Node(name,[domain])])

class FindStatement(Node):
    def __init__(self, name, domain):
        super().__init__("find", [Node(name,[domain])])
    
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
    
##### Expressions
class Expression(Node):
    def __init__(self, label, children = []):
        super().__init__(label, children)

class QuantificationExpression(Node):
    def __init__(self, quantifier, variables, preposition, domain):
        super().__init__(quantifier, [*variables, Node(preposition,[domain])])

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
        self.tokens = re.findall(r'\.\.|\->|\\\/|\/\\|>=|<=|!=|!|==|=|\+|[^=!<>+\s\w]|[\w]+', commentlessStr.replace('\n', ' '))

        print(self.tokens)
        while self.index < len(self.tokens):
            statement = self.parse_statement()
            if statement.info == "NameLettingStatement":
                self.named_constants[statement.label] = statement.children[0]
            if statement.info == "DomainNameLettingStatement":
                self.named_domains[statement.children[0].name] = statement.children[0]
            if statement.info == "FindStatement":    
                self.decision_variables[statement.children[0].name] = statement.children[0]                
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
        letting = self.consume()  # "letting"
        name = self.consume()  # Name
        self.consume()  # "be"
        constant = self.parse_constant()
        nameLetting = Node(name, [constant], "Constant")
        return Node(letting, [nameLetting] , "NameLettingStatement")

    def parse_domain_name_letting_statement(self):
        letting = self.consume()  # "letting"
        name_of_domain = self.consume()  # NameDomain
        self.consume()  # "be "
        self.consume()  # "domain"
        domain = Node(name_of_domain,[self.parse_domain()],"NamedDomain")
        return Node(letting, [domain], "DomainNameLettingStatement")

    def parse_find_statement(self):
        find = self.consume()  # "find"
        name = self.consume()  # Name
        column = self.consume()
        if column != ":":
            raise SyntaxError("Invalid Token - Expected : instead of " + column + " Token Num: " + str(self.index-1))
        domain = self.parse_domain()    
        findVariable = Node(name,[domain], "DecisionVariable")   
        return Node(find, [findVariable],"FindStatement")

    def parse_such_that_statement(self):
        such_that_list = []
        such_that = self.consume()  # "such"
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
        return Node("such that", such_that_list, "SuchThatStatement")

    def parse_domain(self):
        if self.match("int"):
            domain_name = self.consume()  # "int"
            self.consume()  # "("
            lower = self.parse_literal()  # Lower bound
            self.consume()  # ".."
            upper = self.parse_literal()  # Upper bound
            self.consume()  # ")"
            return Node(domain_name, [lower, upper], "IntDomain")
        elif self.match("tuple"):
            domain_name = self.consume()  # "tuple"
            self.consume()  # "("
            domains = []
            while not self.match(")"):
                domains.append(self.parse_domain())
                if self.match(","):
                    self.consume()  # ","
            self.consume()  # ")"
            return Node(domain_name, domains, "TupleDomain")

        elif self.match("relation"):
            domain_name = self.consume()  # "relation"
            self.consume()  # "of"
            self.consume()  # "("
            domains = []
            while not self.match(")"):
                domains.append(self.parse_domain())
                if self.match("*"):
                    self.consume()  # "*"
            self.consume()  # ")"
            return Node(domain_name, domains, "RelationDomain")
        elif self.match("bool"):
            boolDomain = self.consume()  # "bool"            
            return Node(boolDomain, [], "BoolDomain")
        elif self.tokens[self.index] in self.named_domains:
            name_of_domain = self.consume()
            #return NamedDomain(name_of_domain,self.named_domains[name_of_domain].domain) ## TEST
            return Node(name_of_domain, info="ReferenceToNamedDomain")
        else:
            raise SyntaxError("Domain Parsing Error. Token: " + str(self.tokens[self.index]))    

    def match_any(self, tokens):
        return any(self.match(token) for token in tokens)

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
                if self.tokens[self.index] == '[' and self.tokens[self.index +2] == ']':
                    self.consume() # [
                    element = self.parse_literal()
                    self.consume() # ]
                    return Node(identifier, [element], "MemberExpression")
                if self.tokens[self.index] == '(' and self.tokens[self.index +2] == ')':
                    self.consume()  # "("
                    tuple_elements = []
                    while not self.match(")"):
                        tuple_elements.append(Node(self.consume(), info="Literal"))
                        if self.match(","):
                            self.consume()  # ","
                    self.consume()  # ")"
                    return Node(identifier, tuple_elements, "MemberExpression")
            if self.match("(") and self.tokens[self.index + 2] == ",":
                return Node(identifier, [self.parse_tuple_constant()], "MemberExpression") 
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
            or self.index >= len(self.tokens)
        )    
    
    def parse_expression(self):
        ## Quantification
        if self.match_any(["forAll", "exists"]):
             return self.parse_quantification()

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
            
            return 0

        output_queue = []
        operator_stack = []

        while not self.is_expression_terminator():
            if self.match("(") and self.tokens[self.index + 2] != ",":
                operator_stack.append(Node(self.consume(),info="Parenthesis"))  # "("
            elif self.match(")"):
                while operator_stack[-1].name != "(":
                    output_queue.append(operator_stack.pop())
                operator_stack.pop()  # remove the "("
                self.consume()  # ")"
            elif self.checkUnaryOperator(output_queue):
                uOperator = 'u'+self.consume()
                current_operator = Node(uOperator,info="UnaryOperator")
                while (operator_stack and operator_stack[-1].name != "("
                        and precedence(operator_stack[-1].name) > precedence(current_operator.label)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(current_operator)
            elif self.match_any(self.binary_operators):
                current_operator = Node(self.consume(),info="BinaryOperator")
                while (operator_stack and operator_stack[-1].name != "("
                        and precedence(operator_stack[-1].name) >= precedence(current_operator.label)):
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
                stack.append(Node(token.name[-1], [right], "UnaryExpression"))
            elif token.info == "BinaryOperator":
                right = stack.pop()
                left = stack.pop()
                stack.append(Node(token.name, [left,right], "BinaryExpression"))
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
        return Node("Tuple", values, "TupleConstant")

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
        return Node("Relation", values , "RelationConstant")

    def parse_quantification(self):
        quantifier = self.consume()  # "forAll" or "exists"
        variables = []

        while not self.match_any([":", "in"]):
            if self.match("("):
                self.consume()  # "("
                tuple_elements = []
                while not self.match(")"):
                    tuple_elements.append(Node(self.consume(), info="Literal"))
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
        return Node(quantifier, [*variables, Node(preposition, [domain], "Preposition")], "QuantificationExpression")     
    

def buildTreeNX(node, Tree, nodeIndex=None, parent=None):                
    Tree.add_node(id(node), value = node.name, index = nodeIndex) 
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
    info = ""
    if printInfo:
        info = "  #"+ node.info
    print(indent + "+- " + node.name +info)
    extension = ""
    if last:
        extension = "   "
    else:
        extension = "|  "
    indent += extension
    for i in range(len(node.children)):
        printTree(node.children[i], indent, i==len(node.children)-1,printInfo=printInfo)

