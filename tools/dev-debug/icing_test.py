import sys
sys.path.append('../ree/tools')
import tools as ep
import icing

test_strings = []

#test 0
test_strings.append("""
letting a be 5
find i : int(0..(a+1)*(2+3)/-1)
""")
#test 1
test_strings.append("""
letting vertices be domain int(1..3)
letting colours be domain int(1..3)
letting G be relation((1,2),(1,3),(2,3))
letting map be domain relation of (vertices * colours)
letting T be domain tuple (vertices,colours)
find C : map
find t : T
such that
  forAll (u,c) in C .
     forAll (v,d) in C .
        ((u = v) -> (c = d))
such that
  forAll u : vertices .
     exists c : colours . C(u,c)
such that
  forAll (u,v) in G .
     forAll c,d : colours . (C(u,c) /\ C(v,d) -> (c != d))
such that
  t in C
such that
  t[1] = t[2]
""")

for i,test_str in enumerate(test_strings):
    parser = ep.EssenceParser()
    statements = parser.parse(test_str)
    rootTree = ep.Node("Test-" + str(i) , statements, "ROOT")
    ep.printTree(rootTree, printInfo=True)
    spec = icing.ASTtoEssence(rootTree)
    print(spec)