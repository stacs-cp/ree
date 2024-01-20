from EFormatGraph import EFGraph
import EFormatConverters as EFC
import eminipyparser as ep
import networkx as nx
import gp2Interface
import subprocess
import time
import os

# types: Abstract specs(Given+find), instance spec(let+find), parameter or solution(let only)?

class EssenceTransformGraph(EFGraph):
    ''' Essence Transformation Graph.
        Helper function for all transformations of Essence statements
        
        Change of formats via eformat_graph and eformat_converters
        Solve via conjure
        Transformations via GP2

        TODO: Instance Generation from int sequence
        TODO: Solve parameters via int sequence
        TODO:
        '''
    def __init__(self):
        super().__init__() # Format converters are read and initalised here
        parsers = ep.EssenceParser() # one parser one context?
    
    def solve(emini_string):
        params = ""
        conjureCall = ['conjure','solve', emini_string]
        subprocess.run(conjureCall, check=True)
    
    def transform_with_GP2(self,emini_string, program_name):
        gp2string = self.EFG.formatsGraph.FormToForm(emini_string,"Emini","GP2String")
        gp2hostfile = "emini_string.host"
        with open(gp2hostfile, 'w') as file:
            file.write(gp2string)

        # Apply Transform
        hostGraph = os.path.join("gp2",gp2hostfile)
        gp2Interface.runPrecompiledProg(program_name,hostGraph)

        gp2_NEWstring = ""
        # If trasform is applicable solve new spec
        if os.path.isfile("gp2.output"):
            with open("gp2.output") as newGP2spec:
                gp2_NEWstring = newGP2spec.read()
            emini_transformed = self.EFG.formatsGraph.FormToForm(gp2_NEWstring,"GP2String","Emini")
        else:
            return emini_string # The transform has not been applied

        return emini_transformed
    
    def IntSequence_to_Spec(sequence):
        # maybe add to format converter
        emini_string = ""
        return emini_string
    
    def Spec_to_IntSequence(emini_string):
        sequence = []
        return sequence
    
    def normalise(format, spec):
        return
    
    def Abstract_to_ConcreteSpec(abstract_spec,method=""):
        '''
        From a specification with Givens 
        to a specification with only Lettings
        '''
        concrete_spec = ""
        return concrete_spec
    
    def Abstract_to_InstaGen(abstract_spec):
        '''
        From abstract spec 
        to instagen spec
        turns Givens into Finds'''
        insta_gen  = ""
        return insta_gen



g = EssenceTransformGraph()

# Transforms: change format, from int sequence (gen), solve, transform with GP2, normalise, transform with ?.
