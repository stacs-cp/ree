import re
import matplotlib.pyplot as plt
import networkx as nx
import pydot
import copy
from networkx.drawing.nx_pydot import graphviz_layout
from collections import deque

class Node:
    def __init__(self, name, children=[]):
        self.name = name
        self.children = children

class Expression(Node):
    def __init__(self, value):
        super().__init__(value)
        self.value = value

class NameLettingStatement(Node):
    def __init__(self, letting, name, expression):
        super().__init__(letting, [Node(name,[expression])])
        self.name_node = Node(name)
        self.expression = expression

class NamedConstant(Node):
    def __init__(self, name, constant):
        super().__init__(name, [Node(name,[constant])])
        self.constant = constant

class DomainNameLettingStatement(Node):
    def __init__(self, letting, name_of_domain, domain):
        super().__init__(letting, [domain])
        self.name_of_domain = Node(name_of_domain)
        self.domain = domain

class FindStatement(Node):
    def __init__(self, find, name, domain):
        super().__init__(find, [Node(name,[domain])])
        self.name_node = Node(name)
        self.domain = domain

class SuchThatStatement(Node):
    def __init__(self, such_that, expressions):
        super().__init__("such that", expressions)
        self.expression = expressions

class IntDomain(Node):
    def __init__(self, name, lower, upper):
        super().__init__(name, [lower, upper])
        self.lower = Node(lower)
        self.upper = Node(upper)

class TupleDomain(Node):
    def __init__(self, name, domains):
        super().__init__(name, [domains])
        self.domains = domains

class RelationDomain(Node):
    def __init__(self, name, domains):
        super().__init__(name, domains)
        self.domains = domains

class NamedDomain(Node):
    def __init__(self, name, domain):
        super().__init__(name, [domain])
        self.domain = domain

class Operator(Node):
    def __init__(self, name):
        super().__init__(name)
        
class BinaryExpression(Node):
    def __init__(self, left, operator, right):
        super().__init__(operator.name,[left,right])
        self.left = left
        self.operator = operator
        self.right = right

class TupleConstant(Node):
    def __init__(self, values):
        super().__init__("tuple", values)
        self.values = values

class TupleVariable(Node):
    def __init__(self, elements):
        super().__init__('tuple', elements)
        self.elements = elements

class RelationConstant(Node):
    def __init__(self, values):
        super().__init__("relation", values)
        self.values = values

class QuantificationExpression(Node):
    def __init__(self, quantifier, variables, preposition, domain):
        super().__init__(quantifier, [variables, Node(preposition,[domain])] )
        self.variables = variables
        self.preposition = Node(preposition)
        self.domain = domain
        self.quantifier = quantifier

class ConcatenationExpression(Node):
    def __init__(self, left, right):
        super().__init__(" . ", [left, right])
        self.left = left
        self.right = right    

class MemberExpression(Node):
    def __init__(self, identifier, element):
        super().__init__(identifier.name,[element])
        self.identifier = identifier
        self.element = element           


class EssenceParser:
    def __init__(self, input_str):
        self.tokens = re.findall(r'\.\.|\->|\\\/|\/\\|>=|<=|!=|[^\s\w]|[\w]+', input_str.replace('\n', ' '))
        print(self.tokens)
        self.index = 0
        self.named_domains = {} 
        self.named_constants = {}
        self.binary_operators = ["<",">", "<=", ">=", "+", "-", "*", "/", "%", "=","!=", "->", "/\\", "xor","\\/" , "and" , "in"]

    def parse(self):
      statements = []
      while self.index < len(self.tokens):
          statement = self.parse_statement()
          if isinstance(statement, NameLettingStatement):
              self.named_constants[statement.name] = statement.expression
          if isinstance(statement, DomainNameLettingStatement):
              self.named_domains[statement.name_of_domain.name] = statement.domain
          if isinstance(statement, FindStatement):
              self.named_domains[statement.name_node.name] = statement.domain
          
          statements.append(statement)
      return statements

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
        expression = self.parse_constant()
        return NameLettingStatement(letting, name, expression)

    def parse_domain_name_letting_statement(self):
        letting = self.consume()  # "letting"
        name_of_domain = self.consume()  # NameDomain
        self.consume()  # "be "
        self.consume()  # "domain"
        domain = NamedDomain(name_of_domain,self.parse_domain())
        return DomainNameLettingStatement(letting, name_of_domain, domain)

    def parse_find_statement(self):
        find = self.consume()  # "find"
        name = self.consume()  # Name
        colon = self.consume()  # ":"
        domain = self.parse_domain()        
        return FindStatement(find, name, domain)

    def parse_such_that_statement(self):
        such_that_list = []
        such_that = self.consume()  # "such"
        self.consume()  # "that"
        expression = self.parse_expression()

        while self.match_any([".", ',']):
            matched = self.consume()  # "."
            if matched == "." :
                next_expression = self.parse_expression()
                expression = ConcatenationExpression(expression, next_expression)
            else: ## something not working here.
                such_that_list.append(expression)
                expression = self.parse_expression()

        such_that_list.append(expression)
        return SuchThatStatement(such_that, such_that_list)

    def parse_domain(self):
        if self.match("int"):
            domain_name = self.consume()  # "int"
            self.consume()  # "("
            lower = self.parse_literal()  # Lower bound
            self.consume()  # ".."
            upper = self.parse_literal()  # Upper bound
            self.consume()  # ")"
            return IntDomain(domain_name, lower, upper)
        elif self.match("tuple"):
            domain_name = self.consume()  # "tuple"
            self.consume()  # "("
            domains = []
            while not self.match(")"):
                domains.append(self.parse_domain())
                if self.match(","):
                    self.consume()  # ","
            self.consume()  # ")"
            return TupleDomain(domain_name, domains)

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
            return RelationDomain(domain_name, domains)
        elif self.tokens[self.index] in self.named_domains:
            name_of_domain = self.consume()
            #return NamedDomain(name_of_domain,self.named_domains[name_of_domain].domain) ## TEST
            return Node(name_of_domain)
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
            return Expression(self.consume()) ## should it be parse_expression?
        else:
            raise SyntaxError("Invalid constant: " + str(self.tokens[self.index]))

    def parse_literal(self):
        # single integer
        if self.tokens[self.index].isdigit():
            return Expression(self.consume())
        elif self.match("(") and self.tokens[self.index + 2] == ",":            
            return self.parse_tuple_constant()
        else: 
            identifier = Expression(self.consume())
            if self.index +2 < len(self.tokens):
                if self.tokens[self.index] == '[' and self.tokens[self.index +2] == ']':
                    self.consume() # [
                    element = self.parse_literal()
                    self.consume() # ]
                    return MemberExpression(identifier, element)
            if self.match("(") and self.tokens[self.index + 2] == ",":
                return MemberExpression(identifier, self.parse_tuple_constant()) 
            return identifier

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
            if op == "and":
                return -1

            if op == "(":
                return 9


            return 0

        def greater_precedence(op1, op2):
            return precedence(op1) > precedence(op2)

        output_queue = []
        operator_stack = []

        while not self.is_expression_terminator():
            if self.match("(") and self.tokens[self.index + 2] != ",":
                operator_stack.append(Operator(self.consume()))  # "("
            elif self.match(")"):
                while operator_stack[-1].name != "(":
                    output_queue.append(operator_stack.pop())
                operator_stack.pop()  # remove the "("
                self.consume()  # ")"
            elif self.match_any(self.binary_operators):
                current_operator = Operator(self.consume())
                while (operator_stack and operator_stack[-1].name in self.binary_operators
                        and greater_precedence(operator_stack[-1].name, current_operator.name)):
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
            if isinstance(token, Operator):
                right = stack.pop()
                left = stack.pop()
                stack.append(BinaryExpression(left, token, right))
            elif isinstance(token, Node):
                stack.append(token)
            else:
                stack.append(Expression(token))
        return stack[0]    
    
    def parse_tuple_constant(self):
        self.consume()  # "("
        values = []
        while not self.match(")"):
            values.append(Expression(self.consume()))  # Literal 
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
                    tuple_elements.append(Node(self.consume()))
                    if self.match(","):
                        self.consume()  # ","
                self.consume()  # ")"
                variables = TupleVariable(tuple_elements)
            else:
                variables.append(Node(self.consume()))
                if self.match(","):
                    self.consume()  # ","

        preposition = self.consume()  # ":"
        if preposition == ":":
           domain = self.parse_domain()
        else:
           domain = self.parse_literal() ## NEEDS REVISION
        return QuantificationExpression(quantifier, variables,preposition, domain) 

## THIS fixes a display bug that does not like some chars as labels
def labelFix(label):
    fixedLabel = label
    if fixedLabel == "/\\":
      fixedLabel = "AND"
    elif fixedLabel == "\\/":
      fixedLabel = "OR"
    return fixedLabel

def add_nodes_edges(graph, node, parent=None, index=None):    

    unique_id = id(node)

    if index is not None:
        label = f"{node.name} ({index})"
    else:
        label = node.name
        label = labelFix(label)

    graph.add_node(unique_id, label=label)

    if parent:
        graph.add_edge(id(parent), unique_id)

    ## Name
    #if isinstance(node, (NameLettingStatement, FindStatement)):
       # add_nodes_edges(graph, node.name_node, parent=node)

    if isinstance(node, NamedConstant):
        add_nodes_edges(graph, node.constant, parent=node)
    
    if isinstance(node, NameLettingStatement):
        add_nodes_edges(graph, node.name_node, parent=node)
        add_nodes_edges(graph, node.expression, parent=node.name_node)

    if isinstance(node, DomainNameLettingStatement):
        add_nodes_edges(graph, node.name_of_domain, parent=node)
        add_nodes_edges(graph, node.domain.domain, parent=node.name_of_domain)

    if isinstance(node, FindStatement):
        add_nodes_edges(graph, node.domain, parent=node.name_node)
        add_nodes_edges(graph, node.name_node, parent=node)

    if isinstance(node, SuchThatStatement):
        add_nodes_edges(graph, node.expression, parent=node)

    if isinstance(node, IntDomain):
        add_nodes_edges(graph, node.lower, parent=node)
        add_nodes_edges(graph, node.upper, parent=node)

    if isinstance(node, BinaryExpression):
        add_nodes_edges(graph, node.left, parent=node)
        add_nodes_edges(graph, node.right, parent=node)

    if isinstance(node, TupleDomain):
        for index, domain in enumerate(node.domains, start=1):
            add_nodes_edges(graph, domain, parent=node, index=index)

    if isinstance(node, RelationDomain):
        for i, domain in enumerate(node.domains, start=1):
            add_nodes_edges(graph, domain, parent=node, index=i)

    if isinstance(node, TupleConstant):
        for i, value in enumerate(node.values, start=1):
            add_nodes_edges(graph, value, parent=node, index=i)

    if isinstance(node, RelationConstant):
        for i, value in enumerate(node.values, start=1):
            add_nodes_edges(graph, value, parent=node, index=i)


    if isinstance(node, QuantificationExpression):
        # Add quantifier node
        #graph.add_node(node.name)

        # Add variables and edges to the graph
        if  isinstance(node.variables,  TupleVariable):
            add_nodes_edges(graph, node.variables, parent=node)
            add_nodes_edges(graph, node.preposition, parent= node.variables)
            add_nodes_edges(graph, node.domain, parent= node.preposition)
        else:
            for variable in node.variables:
                #print(variable)
                #var_node = Node(variable.name)
                add_nodes_edges(graph, variable, parent=node)
                ##add_nodes_edges(graph, node.preposition, parent=Node(variable.name)) COLUMN symbol causes problems
                ## some fix needed to go from DAG to TREE
                add_nodes_edges(graph, copy.deepcopy(node.domain), parent=variable)

    if isinstance(node, TupleVariable):
        for element in node.elements:
            add_nodes_edges(graph, element, parent=node)

    if isinstance(node, ConcatenationExpression):
        add_nodes_edges(graph, node.left, parent=node)
        add_nodes_edges(graph, node.right, parent=node)

    if isinstance(node, MemberExpression): 
       add_nodes_edges(graph, node.element, parent=node)

        
def createASG(ast):
    G = nx.DiGraph()

    for item in ast:
        add_nodes_edges(G, item)
    
    return G


def printTree(node, indent="", last = True):
    if type(node) != list:
        print(indent + "+- " + node.name )#+ " # " + str(type(node)).split('.')[-1][:-2]) 
        extension = ""
        if last:
            extension = "   "
        else:
            extension = "|  "
        indent += extension
        for i in range(len(node.children)):
            printTree(node.children[i], indent, i==len(node.children)-1)
    else:
        for i in node:
            printTree(i, indent)
