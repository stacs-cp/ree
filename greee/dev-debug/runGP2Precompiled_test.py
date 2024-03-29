import os
import sys
sys.path.append('.')
import greee.gp2Interface as gp2Interface

progName = "gcmulti-func-ChainSawed.gp2"
#progName = "stringTest.gp2"
host = "gcmulti.host"
#host = "gp2Test.host"
hostGraph = os.path.join("gp2",host)
gp2Interface.runPrecompiledProg(progName,hostGraph)