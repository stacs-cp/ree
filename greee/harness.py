#!/usr/bin/env python3
'''
  read spec
   parse arguments
   locate relevant files
   concatenate spec and parameter files
   get AST via Conjure
  benchmark performance
   time running conjure solve
  apply rewriting
   call rewriting system with specified rewrite
   check rewrite actually made a change
  if rewrite happened, benchmark performance of new spec
   concatenate spec and parameter files
  report comparison
'''

import sys
import argparse
import os
import warnings
import pathlib
import atexit
import subprocess

import networkx as nx
import matplotlib.pyplot as plt
import json

#from greee import EFormatConverters as efc

class AST:
    '''
    We use networkx in parallel with our own data structure.
    We therefore assume that edges are added after their nodes,
    to keep our list-based representation in synch with nx.
    '''
    def __init__(self):
        '''
        Make an AST instance.
        '''
        self._ei = 0
        self._edgeLabel = []
        self._edgeFrom = []
        self._edgeTo = []
        self._ni = 0
        self._nodeLabel = []
        self._G = nx.DiGraph()

    def __repr__(self):
        '''
        Make a representation of AST for debugging.
        '''
        return f'<{type(self).__name__} at 0x{id(self):x}, size={len(self)}>'

    def makeEdge(self, u, v, attribute):
        '''
        Create edge u->v with given attribute.
        '''
        self._edgeLabel.append(attribute)
        self._edgeFrom.append(u)
        self._edgeTo.append(v)
        self._G.add_edge(u, v, label=attribute)
        rv = self._ei
        self._ei += 1
        return rv
    def makeNode(self, attribute):
        '''
        Create node with given attribute.
        '''
        self._nodeLabel.append(attribute)
        self._G.add_node(self._ni, label=attribute)
        rv = self._ni
        self._ni += 1
        return rv

    def processSubtree(self, label, value):
        '''
        make a tree with a labelled root node, and deal with its value
        '''
        u = self.makeNode(label)
        if isinstance(value, list):
            w = self.makeNode('list')
            self.makeEdge(u, w, 'child')
            nodeType = 'firstChild'
            prev = w
            n = 0
            for s in value:
                v = self.processSubtree(n, s)
                self.makeEdge(prev, v, nodeType)
                nodeType = 'nextChild'
                prev = v
        elif isinstance(value, dict):
            w = self.makeNode('dict')
            self.makeEdge(u, w, 'child')
            for s,val in value.items():
                v = self.processSubtree(s, val)
                self.makeEdge(w, v, 'child')
        elif isinstance(value, (int, str)):
            # work around dot restrictions on labels
            if value == "/\\":
                value = "AND"
            elif value == "\\/":
                value = "OR"
            v = self.makeNode(value)
            self.makeEdge(u, v, 'child')
        elif value == None:
            v = self.makeNode(value)
            self.makeEdge(u, v, 'child')
        else:
            print('warning, cannot determine type of', value, ' (ignoring)')
        return u

    def printGP2(self, debug):
        '''
        print graph object in GP2 format
        '''
        print('[') # nodes
        n = 0
        for nl in self._nodeLabel:
            print('(', n, ',', nl, ')')
            n += 1
        print('|') # edges
        n = 0
        for l,f,t in zip(self._edgeLabel, self._edgeFrom, self._edgeTo):
            if debug:
                print('(', n, ',', f, ':', self._nodeLabel[f], ',', t, ':', self._nodeLabel[t], ',', l, ')')
            else:
                print('(', n, ',', f, ',', t, ',', l, ')')
            n += 1
        print(']')

    def draw(self, instanceName):
        '''
        Make a PDF representing the AST.
        '''
        from networkx.drawing.nx_agraph import graphviz_layout
        # for looser layout:
        plt.figure(figsize=(20,20), dpi=40)
        pos = graphviz_layout(self._G, prog="dot")
        attributes = nx.get_node_attributes(self._G, 'label')
        nx.draw(self._G, pos, with_labels=True, labels=attributes,
                arrowsize=1.5, width=0.1, node_size=2,
                node_color="lightblue", font_size=2)
        plt.savefig(instanceName+'.pdf')


def harness() -> int:
    '''
    General harness script.
    Put spec and parameter files together, get AST via Conjure.
    '''

    debug = False
    p = argparse.ArgumentParser(description="parse Essence via Conjure and draw AST as PDF")
    p.add_argument('-d', '--debug', action='store_true')
    p.add_argument('file', nargs='+', help='Essence spec or JSON AST, optionally parameter files')
    p.add_argument('-r', '--rewrite', action='store')
    p.add_argument('-j', '--json', action='store_true', help='treat file as AST instead of Essence')
    args = p.parse_args(args=sys.argv[1:])
    debug = args.debug
    if debug: print(args.file, args.rewrite)

    from pathlib import Path
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
                sys.exit('param file ' + str(paramfile) + ' not found, quitting')

    filenames = paramFilenames.copy()
    filenames.append(specfile)
    if debug: print('0:', filenames)

    fn = []
    instanceFileNames = [specfile]
    if args.json:
        warnings.warn('-j specified, ignoring parameter files')
    else:
        instanceFileNames.extend(paramFilenames)
    if debug: print('1:', instanceFileNames)
    for fname in instanceFileNames:
        bname = os.path.basename(fname)
        if bname == '':
            sys.exit('cannot determine ' + str(fname) + ' basename, quitting')
        bname = bname.removesuffix('.essence')
        bname = bname.removesuffix('.param')
        bname = bname.removesuffix('.json')
        fn.append(bname)
    if debug: print('2:', fn)
    instanceName = '-'.join(fn)

# generate temp file name which isn't too horrible when debugging
    tmpfile = './temp-042.essence'
    with open(tmpfile, 'w') as outfile:
        for fname in filenames:
            with open(fname, 'r') as infile:
                outfile.write(infile.read())
    def cleanup():
        '''
        Remove temporary file on exit, unless debugging.
        '''
        if not debug: os.remove(tmpfile)
    atexit.register(cleanup)

# ask conjure to generate AST unless -j was specified
# from spec.bla make spec.bla.astjson
    if args.json:
        astfilename = specfile
    else:
        astfilename = '{0}.astjson'.format(specfile)
        with open(astfilename, 'w') as astfile:
            if subprocess.run(['conjure',
                               'pretty', '--output-format=astjson', tmpfile],
                              shell=False, stdout=astfile).returncode != 0:
                sys.exit('Something went wrong with calling conjure, quitting')

# read JSON representing an Essence spec
    with open(astfilename, 'r') as astfile:
        A = json.load(astfile)

#def read_json_file(filename):
#    with open(filename) as f:
#        js_graph = json.load(f)
#    return json_graph.node_link_graph(js_graph)
#attributes = nx.get_node_attributes(G, 'label')

    G = AST()
    G.processSubtree('root', A)

    if debug: print('nodeLabel=', G._nodeLabel)
    if debug: print('edgeLabel=', G._edgeLabel)
    if debug: print('edgeFrom=', G._edgeFrom)
    if debug: print('edgeTo=', G._edgeTo)

    G.printGP2(debug)
#G.rewriteGP2()
    G.draw(instanceName)

    if debug:
        print(A['mLanguage']['language']['Name']) # Essence
        print(A['mLanguage']['version']) # 1.3
        statements = A['mStatements']
        print(len(statements), "statements")
        for s in statements:
            for keyword in s:
                print(keyword, '=', s[keyword])
            if 'Declaration' in s:
                s2 = s['Declaration']
                print('processing declaration')
                if 'FindOrGiven' in s2:
                    print('processing FindOrGiven')
                    s3 = s2['FindOrGiven']
                    if 'Find' == s3[0]:
                        nameBlob = s3[1]
                        domainBlob = s3[2]
                        print('find', '<', nameBlob['Name'], '>', '<', domainBlob, '>')
                    else:
                        print('not find')
                elif 'Letting' in s2:
                    print('processing Letting')
                else:
                    print('not FindOrGiven or Letting')
            elif 'SuchThat' in s:
                print('processing such that')
            elif 'Where' in s:
                print('processing where')
            elif 'Find' in s:
                print('processing find')

            print()
            if not 'SuchThat' in s: continue
            c = s['SuchThat']
            if not c: continue
            for constraint in c:
                if not 'Op' in constraint: continue
                d = constraint['Op']
                if not d: continue
                if not 'MkOpEq' in d: continue
                e = d['MkOpEq']
                if len(e) != 2: continue
                lhs = e[0]
                rhs = e[1]
                # print(lhs, '=', rhs)
                if len(lhs) == 1 and 'Op' in rhs:
                     rhs = rhs['Op']
                     if 'MkOpSum' in rhs:
                         rhs = rhs['MkOpSum']
                         if not 'AbstractLiteral' in rhs: continue
                         rhs = rhs['AbstractLiteral']['AbsLitMatrix']
                         if len(rhs) == 2:
                             lhs = rhs[0]
                             rhs = rhs[1]
                             print(lhs, '+', rhs)

    '''
    Here are some intended GP2 graphs:
    {'a': {'b': 'c'}} -> (0,a) (1,b) (2,c) | (0,0,1,child) (1,1,2,child)
    No, this is too limited.
    {'a': {'b': 'c'}} -> (0,dict) (1,a) (2,dict) (3,b) (4,c)
                       | (0,0,1,child) (1,1,2,value) (2,2,3,child) (3,3,4,value)
    {a:{b:c}, d:[]} -> (0,dict) (1,a) (2,dict) (3,b) (4,c) (5,d) (6,list)
                     | (0,0,1,child) (1,1,2,value) (2,2,3,child) (3,3,4,value)
                       (4,0,5,child) (5,5,6,value)
    '''

    return 0

if __name__ == '__main__':
    sys.exit(harness())
