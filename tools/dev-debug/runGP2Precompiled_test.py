import os
import sys
sys.path.append('../ree/tools')
import tools.gp2Interface as gp2Interface

progName = "DeMorganTwo.gp2"
hostGraph = os.path.join("gp2","demorgTest.host")
gp2Interface.runPrecompiledProg(progName,hostGraph)