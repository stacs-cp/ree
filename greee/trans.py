#!/usr/bin/env python3
import sys
import argparse
import fileinput
from pathlib import Path
from greee import EFormatGraph
import pickle


def needPickling(format) -> bool:
    '''
    valid formats are:
    Emini ASTpy Json GP2String GP2StringB GP2StringDT GP2Graph NX
    corresponding treatment:
    txt   py    txt  txt       txt        txt         py       py
    '''
    match format:
        case 'ASTpy' | 'GP2Graph' | 'NX':
            return True
        case 'Emini' | 'Json' | 'GP2String' | 'GP2StringB' | 'GP2StringDT':
            return False
        case _:
            sys.exit('unknown format ' + format + ', quitting')


def trans() -> int:
    '''
    General translator frontend

    Usage: trans.py [--from fromFormat] INFILE [--to toFormat] [OUTFILE]
    tries to derive fromFormat from INFILE
    tries to derive toFormat from OUTFILE
    '''

    fromFormat = 'GP2String'
    toFormat = 'Emini'
    EFG = EFormatGraph.EFGraph()
    validFormats = EFG.formsGraph.nodes
    debug = False
    p = argparse.ArgumentParser(description='translate file to another format')
    p.add_argument('-d', '--debug', action='store_true',
        help='print additional diagnostic information')
    p.add_argument('infile', nargs='?', action='store', default='STDIN',
        help='input file')
    p.add_argument('outfile', nargs='?', action='store', default='STDOUT',
        help='output file (required if --toFormat is omitted)')
    p.add_argument('-f', '--fromFormat', action='store', choices=validFormats)
    p.add_argument('-t', '--toFormat', action='store', choices=validFormats)
    args = p.parse_args(args=sys.argv[1:])
    debug = args.debug
    if debug: print(args)
    if args.fromFormat: fromFormat = args.fromFormat
    if args.toFormat: toFormat = args.toFormat
    if args.outfile == 'STDOUT':
        if not args.toFormat:
            sys.exit('--toFormat is required when OUTFILE is absent, quitting')
        if needPickling(toFormat):
            sys.exit('Need an output file with -t ' + toFormat + ', quitting')
    # TODO: allow more relaxed input format names, JSON json Json
    # for each canonical name, check lowercase against lowercase of given format
    # argparse currently enforces strict matching

    if needPickling(fromFormat):
        inObject.new()
        pickle.load(inObject, open('file.pickle', 'rb'))
    else:
        if args.infile == 'STDIN':
            inObject = sys.stdin.read()
        else:
            inObject = open(args.infile).read()
    outObject = EFG.FormToForm(inObject,fromFormat,toFormat)
    if needPickling(toFormat):
        pickle.dump(outObject, open('file.pickle', 'wb'))
    else:
        if args.outfile == 'STDOUT':
            sys.stdout.write(outObject)
        else:
            outf = open(args.outfile)
            outf.write(outObject)
            outf.close()

    return 0

if __name__ == '__main__':
    sys.exit(trans())
