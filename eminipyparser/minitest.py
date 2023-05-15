import ETransformulator as ET

teststr = """
find i : int(0..10)
such that
    1*(2+3*4)-8887=i
"""

ast = ET.EminiToASTpy(teststr)
ET.ep.printTree(ast)
    
gp2z = ET.ASTpyToGP2Graph(ast)
print(gp2z.getGP2String())

nxtree = ET.ASTpyToNX(ast)
print(nxtree.edges(data=True))