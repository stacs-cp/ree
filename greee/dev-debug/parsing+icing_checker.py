import sys
sys.path.append('greee')
import eminipyparser as ep
import os
import icing
from datetime import datetime


def prettyPrintFile(filename):
    with open(filename, 'r') as file:
      data = file.read()
    parser = ep.EssenceParser()
    rootTree = parser.parse(data,filename)
    #rootTree = ep.Node(filename, statements)
    spec = icing.ASTtoEssence(rootTree)
    return (data,spec)

directory = "./tests/"
file = open('./tools/testlogs/icing-log.txt', 'a')
file.write("+++++++++++++++++++++++++++++++++++++ \n")
file.write(str(datetime.now()) + '\n \n')
for filename in os.listdir(directory):
    if filename.endswith(".essence"): 
        try:
          outcome = prettyPrintFile(os.path.join(directory, filename))
          file.write("+++++++++++++++++++++++++++++++++++++ \n")
          file.write(filename + '\n')
          file.write("+++++++++++++ Original ++++++++++++++++ \n")
          file.write(outcome[0] + '\n')
          file.write("* * * * * * Post Icing * * * * * * * \n")
          file.write(outcome[1] + '\n')
        except Exception as e:
          file.write(filename + '\n')
          file.write(str(e) + '\n')
          file.write("----------------------------- \n")
          print("--------------------------------------")
          print("ERROR in: " + filename)
          print(str(e))
          print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
file.close()