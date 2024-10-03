import os
import sys
sys.path.append('.')
import greee.gp2Interface as gp2Interface

progName = "DeMorganTwo.gp2"
#progName = "stringTest.gp2"
host = "DT_test.host"
#host = "gp2Test.host"
hostGraph = os.path.join("gp2",host)
gp2Interface.runPrecompiledProg(progName,hostGraph)