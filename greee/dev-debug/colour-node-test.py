import sys
sys.path.append('.')
from greee import gp2Interface

gp2Interface.compileGP2Program("colour-a-node.gp2")

gp2Interface.runPrecompiledProg("colour-a-node.gp2","/Users/cls29/ree/gp2/constraintset_B.host")
