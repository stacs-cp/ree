import eminipyparser.eminipyparser as ep
import os

input_str = """

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

"""

#parser = ep.EssenceParser(input_str)
#statements = parser.parse()
#rootTree = ep.Node("GraphColouring", statements)
#ep.printTree(rootTree)

def prettyPrintFile(filename):
    with open(filename, 'r') as file:
      data = file.read()
    parser = ep.EssenceParser(data)
    statements = parser.parse()
    rootTree = ep.Node(filename, statements)
    ep.printTree(rootTree)

directory = "./tests/"
for filename in os.listdir(directory):
    if filename.endswith(".essence"): 
        try:
          prettyPrintFile(os.path.join(directory, filename))
        except:
          print("ERROR in: " + filename)


## TODO add test logging