import sys
sys.path.append('greee')
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
given x : int(0..10)                    
where
 x%2=2,
 x>3                  
find y : int(0..100)
such that
x > y
""")

for i,test_str in enumerate(test_strings):
    parser = ep.EssenceParser()
    rootTree = parser.parse(test_str,"Test-" + str(i))
    ep.printTree(rootTree, printInfo=True)