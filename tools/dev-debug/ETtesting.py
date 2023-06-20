import sys
sys.path.append('../ree/tools')
import EFormatConverters as ET
import GP2Graph
import json

teststr = """
find i : int(0..10)
such that
    1*(2+3*4)-8887>i
"""

ast = ET.EminiToASTpy(teststr)
ET.ep.printTree(ast)

j = ET.ASTpyToJson(ast)
print(j)

with open('jsons/data.json', 'w') as f:
    f.write(j)

astfj = ET.JsonToASTpy('jsons/data.json')
ET.ep.printTree(astfj)

astj = json.loads(j, object_hook=lambda ASTpy: ET.ep.Node(**ASTpy))
print("Withoutfilesave")
ET.ep.printTree(astj)

gp2z = ET.ASTpyToGP2Graph(ast)


GP2String = ET.GP2GraphToGP2String(gp2z)# gp2z.getGP2String()
print(GP2String)
gp2g = ET.GP2StringToGP2Graph(GP2String)# GP2Graph.Graph([],[])

#gp2g.graphFromGP2String(GP2String)

ast2 = ET.GP2GraphToASTpy(gp2g)
ET.ep.printTree(ast2, printInfo = True)

spec = ET.ASTpyToEmini(ast2)
print(spec)

astnx = ET.ASTpyToNX(ast2)

gp2fromNX = ET.NXToGP2Graph(astnx)

ast3fromGP2 = ET.GP2GraphToASTpy(gp2fromNX)

ET.ep.printTree(ast3fromGP2)
spec2 = ET.ASTpyToEmini(ast3fromGP2)
print(spec2)