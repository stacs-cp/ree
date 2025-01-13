#!/usr/bin/env python3
'''
Output AST as a pretty-printed tree
'''
import sys
import argparse
import fileinput
from greee import EFormatGraph
import pickle
from greee import eminipyparser as ep
import os


def needPickling(format) -> bool:
    '''
    valid formats and corresponding treatmens:
    Emini ASTpy Json GP2String GP2StringB GP2StringDT GP2Graph NX
    txt   py    txt  txt       txt        txt         py       py
    '''
    match format:
        case 'ASTpy' | 'GP2Graph' | 'NX':
            return True
        case 'Emini' | 'Json' | 'GP2String' | 'GP2StringB' | 'GP2StringDT':
            return False
        case _:
            sys.exit('unknown format ' + format + ', quitting')

def inferKind(f) -> str:
    '''
    Infer what kind of format is likely based on filename.
    '''
    ext = (os.path.splitext(f))[1].lower()
    if debug: print('f =', f, 'ext =', ext)
    match ext:
        case '.host' | '.gp2':
            return 'GP2String'
        case '.json':
            return 'Json'
        case '.nx':
            return 'NX'
        case '.essence' | '.eprime' | '.emini':
            return 'Emini'
        case _:
            return 'unknown'

    #if os.path.isfile(f):
    # TODO: look inside file


def trans() -> int:
    '''
    Pretty-print tree

    Usage: prettyprint.py [--from fromFormat] INFILE
    tries to derive fromFormat from INFILE
    '''

    EFG = EFormatGraph.EFGraph()
    validFormats = EFG.formsGraph.nodes
    global debug
    debug = False
    p = argparse.ArgumentParser(description='pretty-print AST to tree',
        epilog='Example: prettyprint test.essence')
    p.add_argument('-d', '--debug', action='store_true',
        help='print additional diagnostic information')
    p.add_argument('infile', nargs='?', action='store', default='STDIN',
        help='input file')
    p.add_argument('-f', '--fromFormat', action='store', choices=validFormats)
    args = p.parse_args(args=sys.argv[1:])
    debug = args.debug
    if debug: print(args)
    if args.fromFormat: fromFormat = args.fromFormat
    else:
        fromFormat = inferKind(args.infile)
        if fromFormat == 'unknown':
            sys.exit('cannot infer input format, quitting')
    if args.infile != 'STDIN' and not os.path.isfile(args.infile):
        sys.exit('input file ' + args.infile + ' not found, quitting')
    # TODO: allow more relaxed input format names, JSON json Json
    # for each canonical name, check lowercase against lowercase of given format
    # argparse currently enforces strict matching

    if needPickling(fromFormat):
        inObject = []
        inObject = pickle.load(open(args.infile, 'rb'))
    else:
        if args.infile == 'STDIN':
            inObject = sys.stdin.read()
        else:
            inObject = open(args.infile).read()

    AST = EFG.FormToForm(inObject, fromFormat, 'ASTpy')
    ep.printTree(AST)


if __name__ == '__main__':
    sys.exit(trans())
