#!/usr/bin/env python3
import sys
import fileinput
import EFormatGraph

teststr = ''
ETG = EFormatGraph.EFGraph()
with fileinput.input() as f:
    for l in f:
        teststr += l
GP2 = ETG.FormToForm(teststr,"GP2String","Emini")
print(GP2)
