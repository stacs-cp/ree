import sys
sys.path.append('../ree/tools')
import EFormatConverters as ET
import EFormatGraph
import os
import icing
from datetime import datetime

GP2 = """
[ (17, "i~ReferenceToDecisionVariable") (16, "8887~Integer") (15, "4~Integer") (14, "3~Integer") (13, "+~BinaryExpression") 
  (12, "2~Integer") (11, "+~BinaryExpression") (10, "1~Integer") (9, "*~BinaryExpression") (8, "-~BinaryExpression") 
  (7, "=~BinaryExpression") (6, "such that~SuchThatStatement") (5, "10~Integer") (4, "0~Integer") (3, "int~IntDomain") 
  (2, "i~DecisionVariable") (1, "find~FindStatement") (0, "root~Node") |
  (14, 13, 15, 2) (13, 13, 14, 1) (12, 11, 13, 2) 
  (11, 11, 12, 1) (10, 9, 11, 1) (9, 9, 10, 2) 
  (15, 8, 16, 2) (8, 8, 9, 1) (16, 7, 17, 2) 
  (7, 7, 8, 1) (6, 6, 7, 1) (4, 3, 5, 2) 
  (3, 3, 4, 1) (2, 2, 3, 1) (1, 1, 2, 1) 
  (5, 0, 6, 2) (0, 0, 1, 1) ]
"""
ETG = EFormatGraph.ETGraph()
astpy = ETG.FormToForm(GP2,"GP2String","ASTpy")
ET.ep.printTree(astpy, printInfo=True)
Emin = ET.ASTpyToEmini(astpy)
print(Emin)
