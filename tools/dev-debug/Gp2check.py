import sys
sys.path.append('../ree/tools')
import EFormatGraph
import eminipyparser as ep

gp2str = '''
[ (15, "0~Integer") (14, "4~Integer") (13, "i~DecisionVariable") (12, "3~Integer") (11, "such that~SuchThatStatement") 
  (10, "*~BinaryExpression") (9, "1~Integer") (8, "100~Integer") (7, "=~BinaryExpression") (6, "find~FindStatement") 
  (5, "2~Integer") (4, "i~ReferenceToDecisionVariable") (3, "*~BinaryExpression") (2, "int~IntDomain") (1, "root~Node") 
  (0, "+~BinaryExpression") |
  (2, 13, 2, 1) (6, 11, 7, 1) (14, 10, 14, 1) 
  (13, 10, 12, 2) (8, 7, 0, 2) (7, 7, 4, 1) 
  (1, 6, 13, 1) (11, 3, 5, 2) (10, 3, 9, 1) 
  (4, 2, 8, 2) (3, 2, 15, 1) (5, 1, 11, 2) 
  (0, 1, 6, 1) (12, 0, 10, 2) (9, 0, 3, 1) ]'''

ETG = EFormatGraph.ETGraph()
astpy = ETG.FormToForm(gp2str,"GP2String", "ASTpy")
print(astpy) 

ep.printTree(astpy, printInfo=True)