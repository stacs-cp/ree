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
letting X be false
letting Q be true
find P : bool
such that
 (P -> Q) -> X """

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
    candidate_subtrees = findRed(ast)
    if eminipyparser.treeEquality(candidate_subtrees[0],candidate_subtrees[1]):
        for i,child in enumerate(parentFound[0].children):
            content = child.label.split("# ")
            if len(content)>1:
                if content[1] == "grey":
                    # substitute implication with P
                    parentFound[0].children[i] = candidate_subtrees[0]
                    # remove red flag
                    parentFound[0].children[i].label = parentFound[0].children[i].label.split("# ")[0]
                    # remove grey flag
                    parentFound[0].label = parentFound[0].label.split("# ")[0]
            print(parentFound[0])
    else:
        for i,child in enumerate(parentFound[0].children):
            content = child.label.split("# ")
            if len(content)>1:
                if content[1] == "grey":
                    # Add blue flag
                    parentFound[0].children[i].label = parentFound[0].children[i].label.split("# ")[0]
                    parentFound[0].children[i].label += "#blue"
                    # remove grey flag
                    parentFound[0].label = parentFound[0].label.split("# ")[0]
                
            print(parentFound[0])
    

    eminipyparser.printTree(ast)

simplify(new_ast)