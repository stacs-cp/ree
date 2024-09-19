#!/usr/bin/env python3
import sys
import argparse
import fileinput
from pathlib import Path
from greee import EFormatGraph


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
    p.add_argument('infile', action='store',
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
    if args.outfile == 'STDOUT' and not args.toFormat:
        sys.exit('--toFormat is required when OUTFILE is absent, quitting')
    # check valid
    # Emini ASTpy JSON GP2String GP2StringB GP2StringDT GP2Graph NX

    if 0:
        specfile = ''
        paramFilenames = []
        for f in args.file:
            if specfile == '':
                specfile = Path(f)
                if specfile.is_file():
                    if debug: print('found spec file ' + str(specfile))
                else:
                    sys.exit(str(specfile) + ' is not a valid file, quitting')
            else:
                paramfile = Path(f)
                if paramfile.is_file():
                    if debug: print('found param file', paramfile)
                    paramFilenames.append(paramfile)
                else:
                    sys.exit('param file ' + str(paramfile) + ' not found, quitting'
    )

        filenames = paramFilenames.copy()
        filenames.append(specfile)
        if debug: print('0:', filenames)


    teststr = ''
    ETG = EFormatGraph.EFGraph()
    # GP2 = ETG.FormToForm(teststr,fromFormat,toFormat)
    # print(GP2)
    return 0

if __name__ == '__main__':
    sys.exit(trans())
