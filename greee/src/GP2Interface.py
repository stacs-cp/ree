import os
import sys
sys.path.append('../ree/tools')
import subprocess
import EFormatGraph

folder_path = "gp2"

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


def transformSpec_u(gp2prog_file_name, spec):
    ''' 
    Transform a spec using an uncompiled gp2 program.
    '''
    formatsGraph = EFormatGraph.ETGraph()

    gp2spec = formatsGraph.FormToForm(spec,"Emini","GP2String")
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
    Compile and apply all available graph rules to the input spec
    '''
    transforms = scanPrograms()
    specs = []
    for t in transforms:
        new_spec = transformSpec_u(spec,t)
        specs.append([t,new_spec])
    return specs




file_names = scanPrograms()
print(file_names)