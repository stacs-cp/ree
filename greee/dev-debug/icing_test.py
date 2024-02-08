import sys
sys.path.append('greee')
import eminipyparser as ep
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

#test 2
test_strings.append("""
given n : int(1..10)
letting vertices be domain int(1..n)
given edges : set (size 2) of vertices
                    
letting setTest be {0,3,5,n}
""")

test_strings.append("""
given nnodes : int(0..200)
letting Nodes be domain int(0..nnodes)
given graph : set of set (size 2) of Nodes

find MIS : set of Nodes

such that
forAll u,v in graph .
  (u subset MIS) -> !(v subset MIS)
""")

                    
for i,test_str in enumerate(test_strings):
    parser = ep.EssenceParser()
    rootTree = parser.parse(test_str,"Test-" + str(i))
    
    ep.printTree(rootTree, printInfo=True)
    spec = icing.ASTtoEssence(rootTree)
    print(spec)