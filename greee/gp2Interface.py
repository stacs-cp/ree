'''
Helper functions used to interact with GP2
'''

import os
import sys
import shutil
import subprocess
import EFormatGraph

folder_path = "gp2"
compiled_progs_folder = "Compiled"
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

def scanPrecompiledPrograms():
    '''
    Search for all available compiled GP2 programs and return them as list
    
    Returns:
        list: list of all available programs
    '''
    folders = [f.path for f in os.scandir(os.path.join(folder_path, compiled_progs_folder)) if f.is_dir()]
    progs = []
    rules = scanPrograms()
    for rule in rules:
        folder = os.path.join(folder_path, compiled_progs_folder,rule[:-4])
        #Only provide the programs that have a folder a gp2run file in it
        if folder in folders and os.path.isfile(os.path.join(folder, "gp2run")):
            progs.append(rule)
    return progs





def compileGP2Program(gp2prog_file_name):
    """Compile a GP2 program.

    It creates a directory with the same name as the program file, then creates a gp2run executable and copies inside the folder all the .h and .c files from gp2/lib
    

    Args:
        gp2prog_file_name (str): .gp2 file name
    """  
    #Create 'Compiled' folder if it does not exist
    if not os.path.isdir(os.path.join(folder_path, compiled_progs_folder)):
        os.mkdir(os.path.join(folder_path, compiled_progs_folder))

    #Create program folder if it does not exist
    programDir = os.path.join(folder_path,compiled_progs_folder, gp2prog_file_name[:-4])
    if not os.path.exists(programDir):
        os.mkdir(programDir)
    print("Compiling ", gp2prog_file_name)
    try:
        #Call gp2 compiler    
        gp2prog =  os.path.join(folder_path, gp2prog_file_name)    
        gp2CompilerCall = ["gp2","-o", programDir,gp2prog]
        subprocess.run(gp2CompilerCall, check=True)

        #Add all library files to prog folder
        gp2libFiles= os.listdir(lib_dir)
        for file in gp2libFiles:
            shutil.copy2(os.path.join(lib_dir,file), programDir)

        #execute make 
        makeCall = ["make", "-C", programDir]
        subprocess.run(makeCall, check=True)

        print("Compilation Successfull.")

    except Exception as e: 
            print("Compilation Failed.")
            print(e)
            print(repr(e))
            print("Removing program folder...")
            shutil.rmtree(programDir)
    

def runPrecompiledProg(gp2prog_file_name, host):
    """Run graph program on host graph

    Args:
        gp2prog_file_name (str): .gp2 file name
        host (str): .host graph file name
    """    
    programDir = os.path.join(folder_path, compiled_progs_folder, gp2prog_file_name[:-4])

    gp2call = [os.path.join(programDir,"gp2run"), host]
    subprocess.run(gp2call, check=True)


def transformSpec_u(gp2prog_file_name, spec):
    ''' 
    (deprecated)Transform a spec using an uncompiled gp2 program.
    '''
    formatsGraph = EFormatGraph.EFGraph()

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
    '''
    Compiles all the graph programs in the gp2 folder.
    NB: this currently creates a lot of redundant files.
    '''
    ### all programs should be compiled and then used via gp2run instead of gp2c 
    #    
    programs = scanPrograms()
    for prog in programs:
        compileGP2Program(prog)
            

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