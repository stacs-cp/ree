import re
import networkx as nx
import copy

class Node:
    """ Base class for the Nodes of an ASTpy.

        Args:
            label (str): The content of the node
            children (list): children of the node
            info(str, optional): Syntactic information
    """
    def __init__(self, label, children=[],info = ""):
        self.label = label
        self.children = children
        if info == "":
            self.info = str(type(self)).split('.')[-1][:-2] 
        else:
            self.info = info

### Statements
class GivenStatement(Node):
    def __init__(self, name, domain):
        super().__init__("given", [Node(name,[domain], "Parameter")])

class WhereStatement(Node):
    def __init__(self, constraints):
        super().__init__("where", constraints)

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

class SetDomain(Node):
    def __init__(self, domain):
        super().__init__("set", domain)

class FunctionDomain(Node):
    def __init__(self, domains):
        super().__init__("function", domains)

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

class SetConstant(Node):
    def __init__(self, values):
        super().__init__("set", values)

class FunctionConstant(Node):
    def __init__(self, values):
        super().__init__("function", values)

class FunctionItem(Node):
    def __init__(self, left, right):
        super().__init__("functionItem", [left,right])

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
    """ Essence Parser class
    """    
    def __init__(self):
        self.tokens = []
        self.index = 0
        self.parameters = {}
        self.named_domains = {} 
        self.named_constants = {}
        self.decision_variables = {}
        self.binary_operators = ["<",">", "<=", ">=", "+", "-", "*", "/", "%", "=","!=", "->", "/\\", "xor","\\/" , "and" , "in", "subset","subsetEq","intersect","union"]
        self.unary_operators = ["u-","!","utoInt"]
        self.statements = []

    def removeComments(self, spec):
        lines = spec.split('\n')
        newSpec = ""
        for line in lines:
            newSpec += line.split('$',1)[0] + " "
        return newSpec
    
    def parse(self, essenceSpec: str, specname: str = "unnamed") -> Node:
        """
        Parse an Essence specification and returns an Abstract Syntax Tree as nested Node Objects (ASTpy)        

        Args:
            essenceSpec (str): An Essence specification in string format
            specname (str, optional): Name of the spec. Defaults to "unnamed".

        Returns:
            Node: A Node object that is the root of the Abstract Syntax Tree
        """        
        
        commentlessStr = self.removeComments(essenceSpec)
        commentlessStr = commentlessStr.replace(r'/\\n', '/\\')
        self.tokens = re.findall(r'\.\.|-->|\->|\\/|/\\|>=|<=|>|<|!=|!|==|=|\+|[^=!<>+\s\w]|[\w]+', commentlessStr.replace('\n', ' '))

        #print(' '.join(self.tokens))
        #print(len(self.tokens))
        while self.index < len(self.tokens):
            statement = self.parse_statement()
            if statement.info == "GivenStatement":
                self.parameters[statement.children[0].label] = statement.children[0]
            if statement.info == "NameLettingStatement":
                self.named_constants[statement.children[0].label] = statement.children[0]
            if statement.info == "DomainNameLettingStatement":
                self.named_domains[statement.children[0].label] = statement.children[0]
            if statement.info == "FindStatement":    
                self.decision_variables[statement.children[0].label] = statement.children[0]                
            self.statements.append(statement)
        if self.index < len(self.tokens):
            raise Exception("Something went wrong. Parsed until: " + str(self.tokens[self.index]) + " at Token Num: " + str(self.index))
        ASTpy = Node(specname , self.statements, "root")
        return ASTpy

    def consume(self, inputToken=""):
        token = self.tokens[self.index]
        if inputToken != "" and token != inputToken:
            highlighted_token = self.tokens[:]
            highlighted_token.insert(self.index, '\033[31m \033[4m')
            if len(highlighted_token) > self.index + 2:
                highlighted_token.insert(self.index+2, '\033[0m')
            print(' '.join(highlighted_token))
            raise SyntaxError(f"Parsing Error! Token num {self.index}. Expected '{inputToken}', but got '{token}'.") 
        self.index += 1
        return token

    def match(self, expected):
        return self.index < len(self.tokens) and self.tokens[self.index] == expected
    
    def match_any(self, options):
        return self.index < len(self.tokens) and self.tokens[self.index] in options

    def parse_statement(self):
        if self.match("given"):
            return self.parse_given_statement()
        elif self.match("where"):
            return self.parse_where_statement()
        elif self.match("letting"):          
          if self.tokens[self.index + 2] == "be" and self.tokens[self.index + 3] == "domain":
            return self.parse_domain_name_letting_statement()
          if self.tokens[self.index + 2] == "be":
            return self.parse_name_letting_statement()
          else:
              raise SyntaxError("Invalid letting statement: " + str(self.tokens[self.index +2]))
        elif self.match("find"):
            return self.parse_find_statement()
        elif self.match("such"):
            return self.parse_such_that_statement()
        else:
            raise SyntaxError("Invalid statement:" +str( self.tokens[self.index]) + " Token Num: " + str(self.index))

    def parse_given_statement(self):
        self.consume()  # "given"
        name = self.consume()  # Name of parameter
        self.consume(":")
        #if column != ":":
           # raise SyntaxError("Invalid Token - Expected : instead of " + column + " Token Num: " + str(self.index-1))
        domain = self.parse_domain()    
        return GivenStatement(name, domain) 

    def parse_where_statement(self):
        where_list = []
        self.consume()  # "where"
        expression = self.parse_expression()

        while self.match_any([".", ',']):
            matched = self.consume()  # "."
            if matched == "." :
                next_expression = self.parse_expression()
                expression = Node(" . ", [expression, next_expression], "ConcatenationExpression")
            else: ## something not working here. maybe
                where_list.append(expression)
                expression = self.parse_expression()

        where_list.append(expression)
        return WhereStatement(where_list)  

    def parse_name_letting_statement(self):
        self.consume("letting")   
        name = self.consume()  # Name
        self.consume("be")  
        constant = self.parse_constant()
        return NameLettingStatement(name, constant)

    def parse_domain_name_letting_statement(self):
        self.consume("letting")  
        name_of_domain = self.consume()  # NameDomain
        self.consume("be")  
        self.consume("domain") 
        domain = self.parse_domain()
        return DomainNameLettingStatement(name_of_domain, domain)

    def parse_find_statement(self):
        self.consume("find")  # 
        name = self.consume()  # Name
        self.consume(":")
        domain = self.parse_domain()    
        return FindStatement(name, domain)   

    def parse_such_that_statement(self):
        such_that_list = []
        self.consume("such")  
        self.consume("that")
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
            self.consume("int")  
            if not self.match("("):
                print("Warning. Unbounded Int Domain.")
            self.consume("(") 
            lower = self.parse_expression()  # Lower bound
            self.consume("..")  
            upper = self.parse_expression()  # Upper bound
            self.consume(")")  
            return IntDomain(lower,upper)     
               
        elif self.match("tuple"):
            self.consume("tuple")  # "tuple"
            self.consume("(")  # 
            domains = []
            while not self.match(")"):
                domains.append(self.parse_domain())
                if self.match(","):
                    self.consume(",")  # 
            self.consume(")")
            return TupleDomain(domains)

        elif self.match("relation"):
            relation = []
            self.consume("relation") 
            if self.match("("):
                self.consume("(")
                relation.append(self.parse_relation_attribute())
                while self.match(","):
                    self.consume() # ,
                    relation.append(self.parse_relation_attribute())
                self.consume(")") 
            self.consume("of")
            self.consume("(")               
            while not self.match(")"):
                relation.append(self.parse_domain())
                if self.match("*"):
                    self.consume()  # "*"
            self.consume(")") 
            return RelationDomain(relation)
        
        elif self.match("set"):
            set_domain = []
            self.consume("set") # 
            if self.match("("):
                self.consume() # (
                set_domain.append(self.parse_set_attribute())
                while self.match(","):
                    self.consume() # ,
                    set_domain.append(self.parse_set_attribute())
                
                self.consume(")") 
            self.consume("of") 
            set_domain.append(self.parse_domain())
            return SetDomain(set_domain)
        
        elif self.match("function"):
            function_domain = []
            self.consume() # function
            if self.match("("):
                self.consume() # (
                function_domain.append(self.parse_function_attribute())
                while self.match(","):
                    self.consume() # ,
                    function_domain.append(self.parse_function_attribute())
                self.consume(")")
            function_domain.append(self.parse_domain())
            self.consume() # -->
            function_domain.append(self.parse_domain())
            return FunctionDomain(function_domain)

        elif self.match("bool"):
            self.consume()  # "bool"            
            return BoolDomain()
        elif self.tokens[self.index] in self.named_domains:
            name_of_domain = self.consume()
            #return NamedDomain(name_of_domain,self.named_domains[name_of_domain].domain) ## TEST
            return Node(name_of_domain, info="ReferenceToNamedDomain")
        else:
            highlighted_token = self.tokens[:]
            highlighted_token.insert(self.index, '\033[31m \033[4m')
            highlighted_token.insert(self.index+2, '\033[0m')
            print(' '.join(highlighted_token))
            raise SyntaxError("Domain Parsing Error. Token: " + str(self.tokens[self.index])+ ". Token Num: " + str(self.index)) 

    def parse_relation_attribute(self):
        if self.match_any(["size", "minSize","maxSize"]):
            boundKind = self.consume() # size
            size = self.parse_expression() #
            return Node(boundKind, [size], "Attribute")
        elif self.match_any(["reflexive", "irreflexive", "coreflexive", "symmetric", "antiSymmetric", "aSymmetric", 
                             "transitive", "total", "connex", "Euclidean", "serial", "equivalence", "partialOrder"]):
            attribute = self.consume() # 
            return Node(attribute, [], "Attribute")
        else:
            SyntaxError("Relation's Attribute Parsing Error. Current Token: " + str(self.tokens[self.index]))
    
    def parse_set_attribute(self):
        if self.match_any(["size", "minSize","maxSize"]):
            boundKind = self.consume() # size
            size = self.parse_expression() #
            return Node(boundKind, [size], "Attribute")
        else:
            SyntaxError("Set's Attribute Parsing Error. Current Token: " + str(self.tokens[self.index]))

    def parse_function_attribute(self):
        if self.match_any(["size", "minSize","maxSize"]):
            boundKind = self.consume() # size
            size = self.parse_expression() #
            return Node(boundKind, [size], "Attribute")
        elif self.match_any(["injective","surjective","bijective","total"]):
            attribute = self.consume() # 
            return Node(attribute, [], "Attribute")
        else:
            SyntaxError("Function's Attribute Parsing Error. Current Token: " + str(self.tokens[self.index])) 

    def parse_constant(self):
        # tuple - relation - set - function - int - bool
        if self.match("(") and self.tokens[self.index + 2] == ",":
            return self.parse_tuple_constant()        
        elif self.match("relation"):
            return self.parse_relation_constant()
        elif self.match("{"):
            return self.parse_set_constant()
        elif self.match("function"):
            return self.parse_function_constant()
        elif self.tokens[self.index].isdigit():
            return Node(self.consume(),info = "Integer") ## should it be parse_expression?
        elif self.match_any(['true','false']):
            return Node(self.consume(), info="Boolean")
        elif self.match_any(self.named_constants):
            return Node(self.consume(), info="ReferenceToNamedConstant")
        elif self.index + 2 < len(self.tokens) and self.match("(") and self.tokens[self.index + 2] == ")":
                return self.parse_tuple_constant()
        else:
            return self.parse_literal()
            #raise SyntaxError("Invalid constant: " + str(self.tokens[self.index]))

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
            if identifier in self.parameters:
                return Node(identifier, info="ReferenceToParameter")
            if identifier in self.decision_variables:
                return Node(identifier, info="ReferenceToDecisionVariable")
            if identifier in self.named_domains:
                return Node(identifier, info="ReferenceToNamedDomain")
            if identifier in self.named_constants:
                return Node(identifier, info="ReferenceToNamedConstant")
            return Node(identifier, info="Literal")

    def is_expression_terminator(self):
        return (self.index >= len(self.tokens)
            or self.match_any([".",",","given","where","such","letting","find","..","of","-->"])) 
    
    def parse_expression(self):

        ## operators precedence
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
            if op in ["subset","subsetEq"]:
                return 1
            if op in ["intersect", "union"]:
                return 2
            if op in ["+", "-"]:
                return 3
            if op in ["*", "/","%"]:
                return 4
            if op in ["u-", "u!","utoInt"]:   ## UNARY OPERATORS
                return 8
            if op == "(":
                return 9
            
            print("missing operator")
            return 999

        output_queue = []
        operator_stack = []
        parenthesisCount = 0 
        while not self.is_expression_terminator():
            if self.match("(") and self.tokens[self.index + 2] != ",":
                #refactor notes: add recursion here
                parenthesisCount +=1
                operator_stack.append(Node(self.consume(),info="Parenthesis"))  # "("
            elif self.match(")"):
                while operator_stack and operator_stack[-1].label != "(":
                    output_queue.append(operator_stack.pop())
                if operator_stack:
                    operator_stack.pop()  # remove the "("
                parenthesisCount -= 1
                if parenthesisCount < 0:
                    break # encountering a close braket that was never opened is an expression terminator.
                else:
                    self.consume(")")  # ")"
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
            elif self.match_any(["forAll", "exists","sum"]):
                output_queue.append(self.parse_quantification())

            else:
                output_queue.append(self.parse_constant())  # Literal or Name
            
        #print("terminated by:" + str( self.tokens[self.index]))
        while operator_stack:
            output_queue.append(operator_stack.pop())
        return self.build_expression_tree(output_queue)

    def build_expression_tree(self, postfix_expression):
        stack = []
        for token in postfix_expression:            
            if token.info == "UnaryOperator":
                right = stack.pop()              
                stack.append(UnaryExpression(token.label[1:], right))
            elif token.info == "BinaryOperator":
                right = stack.pop()
                left = stack.pop()
                stack.append(BinaryExpression(token.label, left,right))
            elif isinstance(token, Node):
                stack.append(token)
            else:
                stack.append(Node(token))
                print("something not right at " + token + " Token Num: " + str(self.index))
        if len(stack) >0:
            return stack[0]    
        else:
            raise Exception("Missing Expression at: " + str(self.index))

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
        elif self.match("toInt"):
            return True
        else:
            return False
        
    def parse_tuple_constant(self):
        self.consume("(") 
        values = []
        while not self.match(")"):
            values.append(self.parse_literal())  # Literal 
            if self.match(","):
                self.consume()  # ","
        self.consume(")") 
        return TupleConstant(values)

    def parse_relation_constant(self):
        self.consume("relation") 
        self.consume("(") 
        values = []
        while not self.match(")"):
            if self.match("("):
                values.append(self.parse_tuple_constant())
            if self.match(","):
                self.consume(",")
        self.consume(")")  
        return RelationConstant(values)
    
    def parse_set_constant(self):
        self.consume("{")   
        values = []
        while not self.match("}"):
            values.append(self.parse_literal())  # Literal 
            if self.match(","):
                self.consume(",")
        self.consume("}") 
        return SetConstant(values)
    
    def parse_function_constant(self):
        self.consume("function")
        self.consume("(")  
        values = []
        while not self.match(")"):
            values.append(self.parse_function_item())
            if self.match(","):
                self.consume()
        self.consume(")")  # 
        return FunctionConstant(values)
    
    def parse_function_item(self):
        left = self.parse_constant()
        self.consume("-->") # 
        right = self.parse_constant()
        return FunctionItem(left,right)

    def parse_quantification(self):
        quantifier = self.consume()  # "forAll" or "exists" or "sum"
        variables = []

        while not self.match_any([":", "in"]):
            if self.match("("):
                self.consume("(") 
                tuple_elements = []
                while not self.match(")"):
                    tuple_elements.append(Node(self.consume(), info="LocalVariable"))
                    if self.match(","):
                        self.consume(",")  
                self.consume(")")  # 
                variables.append(Node("Tuple", tuple_elements,"TupleVariable"))
            else:
                variables.append(Node(self.consume(), info="LocalVariable"))
                if self.match(","):
                    self.consume(",") 

        preposition = self.consume()  # ":" or "in"
        if preposition == ":":
           domain = self.parse_domain()
        else:
           domain = self.parse_literal() ## TODO NEEDS REVISION
        if self.match("."):
            return QuantificationExpression(quantifier,variables, preposition,domain)
        else:
            raise SyntaxError("Expected . but got: " + str(self.tokens[self.index]))
 

def _buildTreeNX(node, Tree, nodeIndex=None, parent=None):                
    Tree.add_node(id(node), value = node.label, index = nodeIndex) 
    if parent != None: 
        Tree.add_edge(id(parent), id(node))
    for i in range(len(node.children)):
        _buildTreeNX(node.children[i], Tree, i+1, node)

def getNXTree(title = None, Root = []):
    """Returns a NetworkX tree graph from an ASTpy Node

    Args:
        title (str, optional): Name of the spec. Defaults to None.
        Root (list, optional): Root of the ASTpy. Defaults to [].

    Returns:
        nx.DiGraph: Abstract Syntax Tree of an Essence spec as a NetworkX DiGraph 
    """    

    G = nx.DiGraph()
    _buildTreeNX(Root, G)
    return G

def printTree(node, indent="", last = True, printInfo = False):
    """Recursively draw the provided tree as console text from a starting node

    Args:
        node (Node): Input Node object
        indent (str, optional): Current indentation. Defaults to "".
        last (bool, optional): Flag if current node is last child of branch. Defaults to True.
        printInfo (bool, optional): Print addictional syntactic information. Defaults to False.
    """    

    info = ""
    if printInfo:
        info = "  #"+ node.info    
    branch = ""
    extension = ""
    if last:
        branch = "└"
        extension = "   "
    else:
        branch = "├"
        extension = "│  "
    print(indent + branch+"─ " + node.label +info)
    indent += extension
    for i in range(len(node.children)):
        printTree(node.children[i], indent, i==len(node.children)-1,printInfo=printInfo)

def treeEquality(subTree1:Node, subTree2:Node) -> bool: 
  
    """
    Tests if 2 trees are identical all the way down.

    Args:
        subTree1 (Node): First subtree 
        subTree2 (Node): Second subtree 
    Returns:
        bool: returns true if the trees are identical
    """  
    
                
    if subTree1.label != subTree2.label:
        return False
    
    if len(subTree1.children) != len(subTree2.children):
        return False
    else:
        isEqual = True
        for i in range(len(subTree1.children)):
            isEqual = isEqual and treeEquality(subTree1.children[i],subTree1.children[i])
        return isEqual

## ADD treeEquality escluding name of variables. should be sufficient for normalised trees
    
## Potential optimisation: Compare HASHES in memory cache, if hits then check actual tree stored in hard drive.
    