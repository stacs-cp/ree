#!/usr/bin/env python3
import sys
import fileinput
from greee import EFormatGraph

def gp22emini() -> int:
    '''
    Translate GP2 to Emini.
    '''
    teststr = ''
    ETG = EFormatGraph.EFGraph()
    with fileinput.input() as f:
        for l in f:
            teststr += l
    GP2 = ETG.FormToForm(teststr,"GP2String","Emini")
    print(GP2)
    return 0

if __name__ == '__main__':
    sys.exit(gp22emini())
