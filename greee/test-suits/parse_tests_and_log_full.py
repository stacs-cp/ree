import sys
sys.path.append('.')
from greee import eminipyparser as ep
import os
from datetime import datetime

def prettyPrintFile(filename):
    with open(filename, 'r') as file:
      data = file.read()
    parser = ep.EssenceParser()
    statements = parser.parse(data,filename)
    #rootTree = ep.Node(filename, statements)
    ep.printTree(statements,printInfo=True)
    ep.getNXTree(filename,statements)

directory = "./tests/"
errorslogfile = open('./greee/testlogs/errorslog2.txt', 'a')
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