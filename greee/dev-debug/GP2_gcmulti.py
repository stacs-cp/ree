import os
import sys
sys.path.append('.')
import greee.gp2Interface as gp2Interface

progName = "gcmultiRelToFunc4.gp2"
#progName = "stringTest.gp2"
host = "gcmultifunc_B.host"
#host = "gp2Test.host"
hostGraph = os.path.join("gp2",host)
gp2Interface.runPrecompiledProg(progName,hostGraph)