import eminipyparser.eminipyparser2 as ep
import os
from datetime import datetime

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
    parser = ep.EssenceParser()
    statements = parser.parse(data)
    rootTree = ep.Node(filename, statements)
    ep.printTree(rootTree,printInfo=True)
    ep.getNXTree(filename,statements)

directory = "./tests/"
errorslogfile = open('./eminipyparser/testlogs/errorslog2.txt', 'a')
errorslogfile.write("+++++++++++++++++++++++++++++++++++++ \n")
errorslogfile.write(str(datetime.now()) + '\n \n')
for filename in os.listdir(directory):
    if filename.endswith(".essence"): 
        try:
          prettyPrintFile(os.path.join(directory, filename))
        except Exception as e:
          errorslogfile.write(filename + '\n')
          errorslogfile.write(str(e) + '\n')
          errorslogfile.write("----------------------------- \n")
          print("--------------------------------------")
          print("ERROR in: " + filename)
          print(str(e))
errorslogfile.close()