import sys
sys.path.append('../ree/tools')
import eminipyparser as ep

test_strings = []

#test 0
test_strings.append("""
find i : int(0..10)
such that
    1*(2+3*4)+5-6-7=i
""")
#test 1
test_strings.append("""
find i : int(0..10)
such that
    1*(2+3*4)+5-6-a=i
find b : bool
such that
    b != !(true \/ false)
""")
#test 2
test_strings.append("""
letting D be domain int(1..3)
letting Rtype be domain relation of (D * D)
letting R be relation((1,2),(1,3))
find S : Rtype
such that
  forAll (x,y) in S .
     (y,x) in R
, forAll (x,y) in R .
     (y,x) in S

""")
#test 3
test_strings.append("""
find i : int(0..10)
such that
    -(-5)=i-1
""")
#test 4
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
#test 5
test_strings.append("""
find b : bool
such that
    b != !true
""")

#test 6
test_strings.append("""
letting n be 10
letting vertices be domain int (0..(n*n)-1) 
find edges : relation (size 2*(n-1)*n) of (vertices * vertices)
  such that 
    forAll (source,target) in edges .
      source+1 = target /\ (source+1)%n != 0 
      \/  
      source+n = target
""")

for i,test_str in enumerate(test_strings):
    parser = ep.EssenceParser()
    statements = parser.parse(test_str)
    rootTree = ep.Node("Test-" + str(i) , statements, "ROOT")
    ep.printTree(rootTree, printInfo=True)