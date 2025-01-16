#!/usr/bin/env python3
'''
Apply a transformation rule to a spec
'''
import sys
import argparse
import fileinput
#from greee import EFormatGraph
#import pickle
#from greee import eminipyparser as ep
from greee import essence_transforms as et
import os


def applytransform() -> int:
    '''
    Pretty-print tree

    Usage: applytransform.py [INFILE] TRANSFORM
    applies TRANSFORM to spec in INFILE (or STDIN if not supplied)
    '''

    global debug
    debug = False
    p = argparse.ArgumentParser(description='apply transform to spec',
        epilog='Example: applytransform test.essence rewrite.gp2')
    p.add_argument('-d', '--debug', action='store_true',
        help='print additional diagnostic information')
    p.add_argument('infile', nargs='?', action='store', default='STDIN',
        help='input file')
    p.add_argument('rewrite', action='store',
        help='rewrite rule')
    args = p.parse_args(args=sys.argv[1:])
    debug = args.debug
    if debug: print(args)
    if args.infile != 'STDIN' and not os.path.isfile(args.infile):
        sys.exit('input file ' + args.infile + ' not found, quitting')
    infile = args.infile
    rewrite = args.rewrite
    # TODO: allow more relaxed input format names, JSON json Json
    # for each canonical name, check lowercase against lowercase of given format
    # argparse currently enforces strict matching

    ET = et.EssenceTransforms()
    newspec = ET.transform_with_GP2(infile, rewrite)
    print(newspec)


if __name__ == '__main__':
    sys.exit(applytransform())
