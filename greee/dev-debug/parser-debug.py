
import sys
sys.path.append('greee')
import eminipyparser as ep
import time

test_strings = []

#test 0
test_strings.append(r"""
find i : int(0..10)
such that
    1*(2+3*4)+5-6-7=i
""")
#test 1
test_strings.append(r"""
find i : int(0..10)
such that
    1*(2+3*4)+5-6-a=i
find b : bool
such that
    b != !(true \/ false)
""")
#test 2
test_strings.append(r"""
find i : int(0..10)
such that
    (-5)=i
""")
#test 3
test_strings.append(r"""
find i : int(0..10)
such that
    -(-5)=i-1
""")
#test 4
test_strings.append(r"""
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
test_strings.append(r"""
letting G be relation((1,2),(1,3),(2,3))
find x :int(0..100)

such that
 x <= (5+4)+(2+1)
such that
  forAll (u,c) in G . 3
such that
5=5
find b : bool such that b = exists i : int(0..4) . i*i=i
""")
#test 6
test_strings.append(r"""
letting a be domain int(0..10)
find b : int(0..100)
find c : int(0..100)
letting G be relation((1,2),(1,3),(2,3))

such that
 b = sum i : a .1
such that
 c = forAll v in G . v[1] *2
""")
#test 7
test_strings.append(r"""
letting a be true
letting b be false
find c : int(0..10)
such that
  c = toInt(a /\ b)
""")
#test 8
test_strings.append(r"""
given n : int(1..10)
letting vertices be domain int(1..n)
given edges : set (size 2) of vertices
                    
letting setTest be {0,3,5,n}

""")

#test 9
test_strings.append(r"""

letting a be 3
letting intDom be domain int(1..8)
given w : function int(1..10) --> int(1..10)
given g : function set of int(1..0) --> relation (size 8) of (intDom * intDom)
letting fff be function (3-->7,2-->a)
letting ggg be 44                 
find f : function (minSize 2*3, maxSize 18/2+a, total) tuple(intDom,intDom) --> set of int(5..90)
""")

#test_strings = []
#test 10
test_strings.append(r"""

find VAR_0 : relation of (relation of (int(0..10) * int(0..10)) * int(0..10))
""")
#test_strings = []
#test 11
test_strings.append(r"""
given n : int(1..100)
letting vertices be domain int(1..n)
given edges : relation (irreflexive) of ( vertices * vertices )
given numberColours : int(1..n)
given coloursPerNode : int(1..n)
letting colours be domain int(1..numberColours)
letting coloursSet be domain set (size coloursPerNode) of colours
find c : function (total) vertices --> coloursSet
such that
forAll (u,v) in edges .
      (forAll colourAssignment in c .
         (colourAssignment[1] = u) -> !((v,colourAssignment[2]) in c) """)

for i,test_str in enumerate(test_strings):
    try:
      parser = ep.EssenceParser()
      start = time.time_ns()
      ASTpy = parser.parse(test_str,"Test-" + str(i))
      print(time.time_ns()-start)
      ep.printTree(ASTpy, printInfo=True)
      print(hash(test_str))
      print(ep.getNXTree("Test-" + str(i),ASTpy))
    except Exception as e:
          print(str(e))
        