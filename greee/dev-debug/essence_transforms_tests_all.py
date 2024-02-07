import sys
sys.path.append('.')
import subprocess
import os
import pandas as pd
import time
import matplotlib.pyplot as plt
from greee import essence_transforms
import networkx as nx
from datetime import datetime


et = essence_transforms.EssenceTransforms()

def run_all_transforms(filename):
    with open(filename, 'r') as file:
      data = file.read()
    spec_ID = et.add_e_node(data,filename)
    for transform in et.gp2arms:
       et.transform_with_GP2(spec_ID,transform)

directory = "./tests/"
errorslogfile = open('./greee/testlogs/errorslog-transform_all.txt', 'a')
errorslogfile.write("+++++++++++++++++++++++++++++++++++++ \n")
errorslogfile.write(str(datetime.now()) + '\n \n')
for filename in os.listdir(directory):
    if filename.endswith(".essence"): 
        try:
          run_all_transforms(os.path.join(directory, filename))
        except Exception as e:
          errorslogfile.write(filename + '\n')
          errorslogfile.write(str(e) + '\n')
          errorslogfile.write("----------------------------- \n")
          print("--------------------------------------")
          print("ERROR in: " + filename)
          print(str(e))
          print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
errorslogfile.close()