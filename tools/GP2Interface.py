import os
import sys
import shutil
sys.path.append('../ree/tools')
import subprocess
import EFormatGraph

folder_path = "gp2"
lib_dir = os.path.join(folder_path, "lib")

def scanPrograms():
    '''
    Returns all the gp2 programs found in the gp2 folder.
    '''
    gp2_files = []

    # Check if the folder exists
    if os.path.exists(folder_path):
        
        # Loop over all files in the directory
        for filename in os.listdir(folder_path):
            if filename.endswith(".gp2"):
                gp2_files.append(filename)

    return gp2_files


def compileGP2Program(gp2prog_file_name):
    """Compile a GP2 program.

    It creates a directory with the same name as the program file, then creates a gp2run executable and copies inside it all the .h and .c files from gp2/lib
    

    Args:
        gp2prog_file_name (str): .gp2 file name
    """    
    programDir = os.path.join(folder_path, gp2prog_file_name[:-4])
    if not os.path.exists(programDir):
        os.mkdir(programDir)
    gp2prog =  os.path.join(folder_path, gp2prog_file_name)    
    gp2CompilerCall = ["gp2","-o", programDir,gp2prog]
    subprocess.run(gp2CompilerCall, check=True)

    gp2libFiles= os.listdir(lib_dir)
    for file in gp2libFiles:
        shutil.copy2(os.path.join(lib_dir,file), programDir)

    makeCall = ["make", "-C", programDir]
    subprocess.run(makeCall, check=True)

def runPrecompiledProg(gp2prog_file_name, host):
    """Run graph program on host graph

    Args:
        gp2prog_file_name (str): .gp2 file name
        host (str): .host graph file name
    """    
    programDir = os.path.join(folder_path, gp2prog_file_name[:-4])

    gp2call = [os.path.join(programDir,"gp2run"), host]
    subprocess.run(gp2call, check=True)


def transformSpec_u(gp2prog_file_name, spec):
    ''' 
    (deprecated)Transform a spec using an uncompiled gp2 program.
    '''
    formatsGraph = EFormatGraph.ETGraph()

    gp2spec = formatsGraph.FormToForm(spec,"Emini","GP2String")
    #print(gp2spec)
    gp2hostfile = "temporarySpecGraph.host"
    with open(gp2hostfile, 'w') as file:
        file.write(gp2spec)

    gp2prog =  os.path.join(folder_path, gp2prog_file_name)

    gp2cCall = ["gp2c",gp2prog, gp2hostfile]
    subprocess.run(gp2cCall, check=True)

    transformedGP2Spec = ""
    with open("gp2.output") as newGP2spec:
        transformedGP2Spec = newGP2spec.read()

    os.remove("gp2.output")
    os.remove("temporarySpecGraph.host")
    transformedSpec = formatsGraph.FormToForm(transformedGP2Spec,"GP2String","Emini")
    return transformedSpec

def compileGP2folder():
    #TODO
    ### all programs should be compiled and then used via gp2run instead of gp2c 
    #    
    return "TODO"

def allTransformsOnSpec_u(spec):
    '''
    (deprecated)Compile and apply all available graph rules to the input spec
    '''
    transforms = scanPrograms()
    specs = []
    for t in transforms:
        new_spec = transformSpec_u(spec,t)
        specs.append([t,new_spec])
    return specs




#file_names = scanPrograms()
#print(file_names)