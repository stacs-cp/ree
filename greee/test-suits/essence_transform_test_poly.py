import sys
sys.path.append('.')
import subprocess
import os
import pandas as pd
import time
import matplotlib.pyplot as plt
from greee import essence_transforms
import networkx as nx


et = essence_transforms.EssenceTransforms()

spec = r'''find i : int(0..100) $
such that
    i = 1 * 2 + 3 * 4
find a : bool
find b : bool
find c : bool
such that
    a = !(b /\ c)'''

result= et.transform_with_GP2(spec, 'DeMorganTwo.gp2')
print(result)

filespec= "tests/deMorgTest.essence"
result= et.transform_with_GP2(filespec, 'DeMorganTwo.gp2')
print(result)

mynodeID = et.add_e_node(spec)
result= et.transform_with_GP2(mynodeID, 'DeMorganTwo.gp2')



