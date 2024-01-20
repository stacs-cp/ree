import sys
sys.path.append('../ree/tools')
import eminipyparser as ep
import instaGen
import EFormatGraph
test_strings = []

#test 0
test_strings.append("""
given a : int(0..5)
find i : int(0..10)
such that
    1*3=i
""")

#test 1
test_strings.append(r'''
$ graph multicolouring for directed graphs
$ uses exactly coloursPerNode colours for each vert
                    

given n : int(1..100)
letting vertices be domain int(1..n)
given edges : relation (irreflexive) of ( vertices * vertices )
given numberColours : int(1..n)
given coloursPerNode : int(1..numberColours)
letting colours be domain int(1..numberColours)
find c : relation (size n*coloursPerNode) of ( vertices * colours )
such that true

$ endpoints of edges do not share colours
,  forAll (u,v) in edges .
      (forAll colourAssignment in c .
         (colourAssignment[1] = u) -> !((v,colourAssignment[2]) in c))

$ enforce number of colours per node, another version
,  forAll u in vertices .
      coloursPerNode = sum colourAssignment in c .
         toInt(colourAssignment[1] = u)
''')

#test 2
test_strings.append(r'''

                    

given n : int(1..100)
where n%2=0
find x : int(0..50)
''')


ETG = EFormatGraph.EFGraph()

for i,test_str in enumerate(test_strings):
    parser = ep.EssenceParser()
    ASTpy = parser.parse(test_str,"Test-" + str(i))
    ep.printTree(ASTpy, printInfo=True)
    newAST = instaGen.specToInstaGen(ASTpy)
    ep.printTree(newAST, printInfo=True)
    print(ep.getNXTree("Test-" + str(i),newAST))
    print(ETG.FormToForm(newAST,"ASTpy","Emini"))
