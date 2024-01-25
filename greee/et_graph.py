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
    """ Essence Transformation Graph.
        Helper function for all transformations of Essence statements.
        Nodes are Essence statemente in Emini format, edges are records of transformations.
        
        Change of formats via eformat_graph and eformat_converters
        Solve via conjure
        Transformations via GP2

        TODO: Instance Generation from int sequence
        TODO: Solve parameters via int sequence
        TODO:
        """
    def __init__(self):
        super().__init__() # Format converters are read and initalised here
        self.parser = ep.EssenceParser() # one parser one context?
        self.graph = nx.MultiDiGraph()

    def add_e_node(self, emini_string, file_name=""):            
        """Add a node to the graph, the hash of the input emini_string is computed and used as ID

        Args:
            emini_string (string): Emini specification in string format
            file_name (str, optional): Name of file if it exists. Defaults to "" if it doesn't.
        
        Returns:
            Int: ID of the node
        """
        ID = hash(emini_string)
        self.graph.add_node(ID, emini=emini_string,file_name=file_name)
        return ID
    
    def add_e_edge(self, source, target, transformation_name, data ={}):
        """ add an edge to the graph, source and target are IDs of nodes.
        The transformation name is required. An arbitrary data dictionary can be appended as attributes.
        Args:
            source (int): Source ID
            target (int): Target ID
            transformation_name (string): Name of the transformation
            data (dict, optional): Optional attributes. Defaults to {}.
        """        
        attributes = {'transformation': transformation_name, **data}
        self.graph.add_edge(source, target, attr=attributes)
    
    def solve(self, ID):
        if self.graph.nodes[ID]['file_name'] == "":
            specFilename = f"./tests/{hex(ID)}.essence"
            with open(specFilename, 'w') as file:
                file.write(self.graph.nodes[ID]['emini'])
            self.graph.nodes[ID]['file_name'] = specFilename

        params = ""
        conjureCall = ['conjure','solve', self.graph.nodes[ID]['file_name']]
        subprocess.run(conjureCall, check=True)
        try:
            with open("./conjure-output/model000001-solution000001.solution") as solution:
                s = solution.read()
            solution_ID = self.add_e_node(s)
            self.add_e_edge(ID,solution_ID,"solved")
        except:
            print("error while reading solution")
        return  s
            


    def solve_from_file(self, file_name):
        '''
        Call conjure and return solution as string
        '''
        params = ""
        conjureCall = ['conjure','solve', file_name]
        subprocess.run(conjureCall, check=True)
        try:
            with open("./conjure-output/model000001-solution000001.solution") as solution:
                s = solution.read()
        except:
            print("error while reading solution")
        return  s
    
    def transform_with_GP2(self,emini_string, program_name):
        gp2string = self.FormToForm(emini_string,"Emini","GP2String")
        gp2hostfile = "emini_string.host"
        with open(gp2hostfile, 'w') as file:
            file.write(gp2string)

        # Apply Transform
        #hostGraph = os.path.join("gp2",gp2hostfile)
        gp2Interface.runPrecompiledProg(program_name,gp2hostfile)

        gp2_NEWstring = ""
        # If trasform is applicable solve new spec
        if os.path.isfile("gp2.output"):
            with open("gp2.output") as newGP2spec:
                gp2_NEWstring = newGP2spec.read()
            emini_transformed = self.FormToForm(gp2_NEWstring,"GP2String","Emini")
              # Clear files
            os.remove("gp2.output")
            
        else:
            print(f"Transform {program_name} not applied")
            emini_transformed = emini_string # The transform has not been applied

        if os.path.isfile("gp2.log"):
                os.remove("gp2.log")
        os.remove(gp2hostfile)

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



# Transforms: change format, from int sequence (gen), solve, transform with GP2, normalise, transform with ?.
