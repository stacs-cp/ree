import eminipyparser2 as ep
import os
from datetime import datetime
import matplotlib.pyplot as plt
import networkx as nx
input_str = """

letting vertices be domain int(1..3)
letting colours be domain int(1..3)
letting G be relation((1,2),(1,3),(2,3))
find C : relation of (vertices * colours) $ a function, really
such that
  $ function
  forAll (u,c) in C .
     forAll (v,d) in C .
        ((u = v) -> (c = d))
  $ total
, forAll u : vertices .
     exists c : colours . C(u,c)
  $ proper colouring
, forAll (u,v) in G .
     forAll c,d : colours . (C(u,c) /\ C(v,d) -> (c != d))



"""

parser = ep.EssenceParser()
statements = parser.parse(input_str)
rootTree = ep.Node("GraphColouring", statements)
ep.printTree(rootTree, printInfo=True)

G = ep.getNXTree("GraphColouring", statements)
