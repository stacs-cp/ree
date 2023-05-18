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

nxtree = ET.ASTpyToNX(ast)
print(nxtree.edges(data=True))

for v,node in nxtree.nodes(data=True):
    print("--------")
    print(node)

for u,v,data in nxtree.edges(data = True):
    print(u,v,data)


mystr = '''
[
    (0, "abc":"def":"ghi":"jkl")
    (1, 2:"mnopqrstuvwxyz")
    ('2', 1:'"one"':2:"two")
    (3, 6:6:6:6:6:6:6:6:6:6:6:6:6)
    (4, empty)
|
    (0, 0, 1, 0)
    (1, 0, 1, 0 # red)
    (2, 0, 2, "2" # blue)
    (3, 1, 3, empty # dashed)
    (4, 2, 2, empty # green)
    (4, 2, 2, empty)
    (5, 2, 3, 'empty # red)
    (6, 2, 4, 6:6:6:6:5:6:6)
    (7, 2, 4, 6:6:6:6:5:6:6 # dashed)
] '''

g = GP2Graph.Graph()
g.graphFromGP2String(mystr)
print(g.getGP2String())
h = GP2Graph.Graph([],[])
h.graphFromGP2String(g.getGP2String())
print(h.getGP2String())