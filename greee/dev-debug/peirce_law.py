import os
import sys
sys.path.append('.')
from greee import gp2Interface
from greee import EFormatGraph
from greee import essence_transforms
from greee import eminipyparser
progName = "peirce.gp2"

gp2Interface.compileGP2Program(progName)

peirce_test = r"""
letting Q be true
find P : bool
such that
 (P -> Q) -> P """

EFG = EFormatGraph.EFGraph()
ast1 = EFG.FormToForm(peirce_test, "Emini","ASTpy")
eminipyparser.printTree(ast1)

gp2g = EFG.FormToForm(peirce_test, "Emini","GP2StringB")
filename= "pierce_test_file.host"
with open(filename, "w") as f:
    f.write(gp2g)
gp2Interface.runPrecompiledProg(progName,filename)

with open("gp2.output", "r") as f:
    new_ast_gp2 = f.read()

new_ast = EFG.FormToForm(new_ast_gp2, "GP2StringB", "ASTpy")

eminipyparser.printTree(new_ast)

def simplify(ast):
    def findRed(node, found=[]):
        content = node.label.split("# ")
        if len(content)>1:
            if content[1] == "red":
                found.append(node)
        for n in node.children:
            findRed(n,found)
        return found

    def findGrey(node, found=[]):
        content = node.label.split("# ")
        if len(content)>1:
            if content[1] == "grey":
                found.append(node)
                print(node)
        for n in node.children:
            findGrey(n,found)
        return found

    parentFound = findGrey(new_ast)
    for i,found in enumerate(parentFound):
        print(i,found)
    for i,child in enumerate(parentFound[0].children):
        content = child.label.split("# ")
        if len(content)>1:
            if content[1] == "grey":
                parentFound[0].children[i] = findRed(ast)[0]
        print(parentFound[0])

    eminipyparser.printTree(ast)

simplify(new_ast)