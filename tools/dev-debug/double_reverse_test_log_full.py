import sys
sys.path.append('../ree/tools')
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

    # check equality of strings and trees
    sameSynthSpecs = synthSpec2 == synthSpec4
    sameTrees = treeEquality(rootTree1, rootTree3)

    return (sameSynthSpecs,sameTrees,rootTree1,rootTree3,synthSpec2,synthSpec4)

  
def treeEquality(subTree1, subTree2):                
  if subTree1.label != subTree2.label:
      return False
  
  if len(subTree1.children) != len(subTree2.children):
      return False
  elif len(subTree1.children) > 0 and len(subTree2.children) > 0:
    isEqual = True
    for i in range(len(subTree1.children)):
      isEqual = isEqual and treeEquality(subTree1.children[i],subTree1.children[i])
    return isEqual
  elif len(subTree1.children) == 0 and len(subTree2.children) == 0:
      return True

      
def runAndLogFullTest():
  directory = "./tests/"
  file = open('./tools/testlogs/doubleReverseTest-log.txt', 'a')
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

def testTheTestFunction():

  spec1 = """
  find i : int(0..10)
  such that
      1*(2+3*4)+5-6-7=i
  """

  spec2 = """
  find i : int(0..10)
  such that
      1*(2+3*4)+5-6-a=i
  find b : bool
  such that
      b != !(true \/ false)
  """
  # Essence to AST 
  parser1 = ep.EssenceParser()
  statements1 = parser1.parse(spec1)
  rootTree1 = ep.Node("TestSpec1", statements1)    

  # AST to Synth Essence
  synthSpec2 = icing.ASTtoEssence(rootTree1)
  
  ## Synth Essence to AST
  parser3 = ep.EssenceParser()
  statements3 = parser3.parse(spec2)
  rootTree3 = ep.Node("TestSpec2", statements3) 

  ## AST to synth Essence 
  synthSpec4 = icing.ASTtoEssence(rootTree3)

  # check equality of strings and trees
  sameSynthSpecs = synthSpec2 == synthSpec4
  sameTrees = treeEquality(rootTree1, rootTree3)
  print("SameText: "+ str(sameSynthSpecs))
  print("SameTree: "+ str(sameTrees))
  print("SanityCheck: "+str(treeEquality(rootTree1, rootTree1)))
  print("SanityCheck2: "+str(treeEquality(rootTree3, rootTree3)))

testTheTestFunction()