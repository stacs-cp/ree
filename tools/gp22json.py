#!/usr/bin/env python3
import sys
import fileinput
sys.path.append('tools')
import EFormatGraph

teststr = ''
ETG = EFormatGraph.EFGraph()
with fileinput.input() as f:
    for l in f:
        teststr += l
GP2 = ETG.FormToForm(teststr,"GP2String","Json")
print(GP2)
