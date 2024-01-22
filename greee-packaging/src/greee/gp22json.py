#!/usr/bin/env python3
import sys
import fileinput
#sys.path.append('tools')
from greee import EFormatGraph

def gp22json() -> int:
    '''
    Translate GP2 to JSON.
    '''
    teststr = ''
    ETG = EFormatGraph.ETGraph()
    with fileinput.input() as f:
        for l in f:
            teststr += l
    GP2 = ETG.FormToForm(teststr,"GP2String","Json")
    print(GP2)
    return 0

if __name__ == '__main__':
    sys.exit(gp22json())
