import sys
sys.path.append('../ree/tools')
import EFormatGraph
import eminipyparser as ep

gp2str = '''
[ (18, "NOT~UnaryExpression") (17, "NOT~UnaryExpression") (16, "c~ReferenceToDecisionVariable") (15, "b~ReferenceToDecisionVariable") (13, "OR~BinaryExpression") 
  (12, "a~ReferenceToDecisionVariable") (11, "=~BinaryExpression") (10, "such that~SuchThatStatement") (9, "bool~BoolDomain") (8, "c~DecisionVariable") 
  (7, "find~FindStatement") (6, "bool~BoolDomain") (5, "b~DecisionVariable") (4, "find~FindStatement") (3, "bool~BoolDomain") 
  (2, "a~DecisionVariable") (1, "find~FindStatement") (0, "root~Node") |
  (19, 18, 16, 1) (18, 17, 15, 1) (17, 13, 18, 2) 
  (16, 13, 17, 1) (12, 11, 13, 2) (11, 11, 12, 1) 
  (10, 10, 11, 1) (8, 8, 9, 1) (7, 7, 8, 1) 
  (5, 5, 6, 1) (4, 4, 5, 1) (2, 2, 3, 1) 
  (1, 1, 2, 1) (9, 0, 10, 4) (6, 0, 7, 3) 
  (3, 0, 4, 2) (0, 0, 1, 1) ]'''

ETG = EFormatGraph.EFGraph()
astpy = ETG.FormToForm(gp2str,"GP2String", "ASTpy")
print(astpy) 

ep.printTree(astpy, printInfo=True)
spec = ETG.FormToForm(astpy,"ASTpy", "Emini")
print(spec)