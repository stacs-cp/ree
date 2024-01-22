import sys
sys.path.append('greee')
import EFormatConverters as EFC
import greee.gp2Graph as gp2Graph
import json

teststr = """
find i : int(0..10)
such that
    1*(2+3*4)-8887>i
"""

ast = EFC.EminiToASTpy(teststr)
EFC.ep.printTree(ast)

j = EFC.ASTpyToJson(ast)
print(j)

with open('jsons/data.json', 'w') as f:
    f.write(j)

astfj = EFC.JsonToASTpy('jsons/data.json')
EFC.ep.printTree(astfj)

astj = json.loads(j, object_hook=lambda ASTpy: EFC.ep.Node(**ASTpy))
print("Withoutfilesave")
EFC.ep.printTree(astj)

gp2z = EFC.ASTpyToGP2Graph(ast)


GP2String = EFC.GP2GraphToGP2String(gp2z)# gp2z.getGP2String()
print(GP2String)
gp2g = EFC.GP2StringToGP2Graph(GP2String)# GP2Graph.Graph([],[])

#gp2g.graphFromGP2String(GP2String)

ast2 = EFC.GP2GraphToASTpy(gp2g)
EFC.ep.printTree(ast2, printInfo = True)

spec = EFC.ASTpyToEmini(ast2)
print(spec)

astnx = EFC.ASTpyToNX(ast2)

gp2fromNX = EFC.NXToGP2Graph(astnx)

ast3fromGP2 = EFC.GP2GraphToASTpy(gp2fromNX)

EFC.ep.printTree(ast3fromGP2)
spec2 = EFC.ASTpyToEmini(ast3fromGP2)
print(spec2)