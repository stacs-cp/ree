import ETransformulator as ET
import GP2Graph

teststr = """
find i : int(0..10)
such that
    1*(2+3*4)-8887=i
"""

ast = ET.EminiToASTpy(teststr)
ET.ep.printTree(ast)
    
gp2z = ET.ASTpyToGP2Graph(ast)
print(gp2z.getGP2String())

GP2String = gp2z.getGP2String()

gp2g = GP2Graph.Graph([],[])

gp2g.graphFromGP2String(GP2String)

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