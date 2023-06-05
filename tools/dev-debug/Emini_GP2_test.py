import sys
sys.path.append('../ree/tools')
import EFormatGraph


eminiSpec = """
find i : int(0..10)
such that
    1*(2+3*4)-8887=i
"""

# translate to GP2
ETG = EFormatGraph.ETGraph()
GP2 = ETG.FormToForm(eminiSpec,"Emini","GP2String")
print(GP2) 

## Copy the result of the transform into this string
GP2transformed = """
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

# convert back to Emini
backToEmini = ETG.FormToForm(GP2transformed,"GP2String","Emini")
print(backToEmini)


## Place holder - Program used for the transformation in GP2
gp2_program = '''
Main = commute

commute(operator,operand1, operand2:string)
[
    (n1, operator)
    (n2, operand1)
    (n3, operand2)
    |
    (e1, n1, n2, 1)
    (e2, n1, n3, 2)
]
=>
[
    (n1, operator)
    (n2, operand1)
    (n3, operand2)
    |
    (e1, n1, n2, 2)
    (e2, n1, n3, 1)
]
interface = 
{
    n1, n2, n3
}
where operator = "*~BinaryExpression"
'''