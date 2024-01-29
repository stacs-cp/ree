#!/usr/bin/env python3
import sys
import fileinput
from greee import EFormatGraph

def emini2gp2() -> int:
    '''
    Translate Emini to GP2.
    Multiple files can be provided.
    This is usually one spec and some associated parameter files.
    '''
    teststr = ''
    ETG = EFormatGraph.EFGraph()
    with fileinput.input() as f:
        for l in f:
            teststr += l
    GP2 = ETG.FormToForm(teststr,"Emini","GP2String")
    print(GP2)
    return 0

if __name__ == '__main__':
    sys.exit(emini2gp2())
