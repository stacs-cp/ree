import eminipyparser as ep
import os
import icing
from datetime import datetime


def doubleReverseTest(filename):
    '''
    Transform an essence spec into AST
    Then synthetise the Essence spec from the AST
    Tranform the synthetic Essence spec again into AST
    Compare the 2 trees
    Synthetise a new Essence spec from the second tree
    Compare the 2 synthetic specs'''
    with open(filename, 'r') as file:
      originalSpec = file.read()

    # Essence to AST 
    parser1 = ep.EssenceParser()
    statements1 = parser1.parse(originalSpec)
    rootTree1 = ep.Node(filename, statements1)    

    # AST to Synth Essence
    synthSpec2 = icing.ASTtoEssence(rootTree1)
    
    ## Synth Essence to AST
    parser3 = ep.EssenceParser()
    statements3 = parser3.parse(synthSpec2)
    rootTree3 = ep.Node(filename, statements3) 

    ## AST to synth Essence 
    synthSpec4 = icing.ASTtoEssence(rootTree3)

    sameSynthSpecs = synthSpec2 == synthSpec4
    sameTrees = rootTree1 == rootTree3

    return (sameSynthSpecs,sameTrees,rootTree1,rootTree3,synthSpec2,synthSpec4)

directory = "./tests/"
file = open('./eminipyparser/testlogs/doubleReverseTest-log.txt', 'a')
file.write("+++++++++++++++++++++++++++++++++++++ \n")
file.write(str(datetime.now()) + '\n \n')
for filename in os.listdir(directory):
    if filename.endswith(".essence"): 
        try:
          outcome = doubleReverseTest(os.path.join(directory, filename))
          file.write("+++++++++++++++++++++++++++++++++++++ \n")
          file.write(filename + '\n')
          file.write("Same Spec: "+ str(outcome[0] )+ '\n')
          file.write("Same Tree: "+ str(outcome[1] )+ "\n")

          if outcome[1] == False:
             print("++++++ Tree From Original")
             ep.printTree(outcome[2], printInfo=True)
             print("------Tree From Synth Spec")
             ep.printTree(outcome[3], printInfo=True)
            

        except Exception as e:
          file.write("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n")
          file.write(filename + '\n')
          file.write(str(e) + '\n')
          file.write("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ \n")
          print("--------------------------------------")
          print("ERROR in: " + filename)
          print(str(e))
          print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
file.close()