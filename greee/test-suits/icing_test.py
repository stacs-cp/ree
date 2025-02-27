import sys
sys.path.append('.')
import greee.eminipyparser as ep
from greee import icing

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

test_strings.append(r"""
given nnodes : int(0..200)
letting tup be (3,5)
letting mySet be {tup}
letting Nodes be domain int(0..nnodes)
given graph : set of set (size 2) of Nodes

find MIS : set of Nodes

such that
forAll u,v in graph .
  (u subset MIS) -> !(v subset MIS)
""")

test_strings.append(r"""

letting a be 3
letting intDom be domain int(1..8)
given w : function int(1..10) --> int(1..10)
given g : function set of int(1..0) --> relation (size 8) of (intDom * intDom)
letting fff be function (3-->7,2-->a)
letting ggg be 44                 
find f : function (minSize 2*3, maxSize 18/2+a, total) tuple(intDom,intDom) --> set of int(5..90)

""")

test_strings.append(r"""

given n : int(0..100)
letting vertices be domain int(0..n-1)
given edges : relation (irreflexive) of ( vertices * vertices )
given numberColours : int(1..n)
given coloursPerNode : int(1..n)
letting colours be domain int(1..numberColours)
letting coloursSet be domain set (size coloursPerNode) of colours
find c : function (total) vertices --> coloursSet
such that
forAll (u,v) in edges .
      c(v) intersect c(u) = {}

""")

test_strings.append(r"""

given n : int(1..100)
letting vertices be domain int(0..n-1)
given edges : relation (irreflexive) of ( vertices * vertices )
given numberColours : int(1..n)
given coloursPerNode : int(1..n)
letting colours be domain int(1..numberColours)
find c : relation (size n*coloursPerNode) of ( vertices * colours )
such that

$ endpoints of edges do not share colours
forAll (u,v) in edges .
      (forAll colourAssignment in c .
         (colourAssignment[1] = u) -> !((v,colourAssignment[2]) in c))

$ enforce number of colours per node, another version
,  forAll u : vertices .
      coloursPerNode = (sum colourAssignment in c .
         toInt(colourAssignment[1] = u))

""")



                    
for i,test_str in enumerate(test_strings):
    parser = ep.EssenceParser()
    rootTree = parser.parse(test_str,"Test-" + str(i))
    
    ep.printTree(rootTree, printInfo=True)
    spec = icing.ASTtoEssence(rootTree)
    print(spec)