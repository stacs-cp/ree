
import sys
sys.path.append('../ree/tools')
import eminipyparser as ep
import os
import icing
from datetime import datetime

def prettyPrintFile(filename):
    with open(filename, 'r') as file:
      data = file.read()
    parser = ep.EssenceParser()
    statements = parser.parse(data)
    rootTree = ep.Node(filename, statements)
    ep.printTree(rootTree,printInfo=True)
    ep.getNXTree(filename,statements)
    spec = icing.ASTtoEssence(rootTree)
    print(spec)

directory = "./tests/"
errorslogfile = open('./tools/testlogs/errorslog-parse+icing.txt', 'a')
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
          print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
errorslogfile.close()