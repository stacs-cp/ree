import os
import sys
sys.path.append('../ree/tools')
import GP2Interface

progName = "DeMorganTwo.gp2"
hostGraph = os.path.join("gp2","demorgTest.host")
GP2Interface.runPrecompiledProg(progName,hostGraph)