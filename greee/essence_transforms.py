from greee.EFormatGraph import EFGraph
from greee import EFormatConverters as EFC
from greee import eminipyparser as ep
import networkx as nx
from greee import gp2Interface
from greee import normalisers
import subprocess
from greee import instaGen
import random
import numpy as np
import time
import os

# types: Abstract specs(Given+find), instance spec(let+find), parameter or solution(let only)?

class EssenceTransforms(EFGraph):
    """ Essence Transformation Graph.
        Helper function for all transformations of Essence statements.
        Nodes are Essence statemente in Emini format, edges are records of transformations.
        
        Change of formats via eformat_graph and eformat_converters
        Solve via conjure
        Transformations via GP2

        TODO: Instance Generation from int sequence
        TODO: Solve parameters via int sequence
        TODO: Spec2Vec?
        """
    def __init__(self):
        super().__init__() # Format converters are gathered and initalised here
        self.parser = ep.EssenceParser() # one parser one context?
        self.graph = nx.MultiDiGraph()
        self.gp2arms = gp2Interface.scanPrecompiledPrograms()
        self.epsilon = 0.5 # exploration parameter for multi armed bandit

    def add_e_node(self, emini_string, file_name=""):            
        """Add a node to the graph, the hash of the input emini_string is computed and used as ID

        Args:
            emini_string (str): Emini specification in string format
            file_name (str, optional): Name of file if it exists. Defaults to "" if it doesn't.
        
        Returns:
            int: ID of the node
        """
        ID = abs(hash(emini_string)) #change hashing function to something better
        if ID not in self.graph:
            self.graph.add_node(ID, emini=emini_string,file_name=file_name)
        return ID
    
    def add_e_edge(self, source, target, transformation_name, data ={}):
        """ add an edge to the graph, source and target are IDs of nodes.
        The transformation name is required. An arbitrary data dictionary can be appended as attributes.
        Args:
            source (str): Source ID
            target (str): Target ID
            transformation_name (str): Name of the transformation
            data (dict, optional): Optional attributes. Defaults to {}.
        """        
        attributes = {'transformation': transformation_name, **data}
        self.graph.add_edge(source, target, None, **attributes)
    
    def solve(self, ID):
        if self.graph.nodes[ID]['file_name'] == "":
            specFilename = f"{hex(ID)}.essence"
            with open(specFilename, 'w') as file:
                file.write(self.graph.nodes[ID]['emini'])
            self.graph.nodes[ID]['file_name'] = specFilename

        params = ""
        conjureCall = ['conjure','solve', self.graph.nodes[ID]['file_name']]
        subprocess.run(conjureCall, check=True)
        try:
            solution_file= self.graph.nodes[ID]['file_name'][:-7]+'solution'
            with open(solution_file) as solution:
                s = solution.read()
            solution_ID = self.add_e_node(s,solution_file)
            self.add_e_edge(ID,solution_ID,"solution")
        except:
            # ADD crash node here?
            print("error while reading solution")
            print("Spec file:", specFilename)
        return  s
            


    def solve_from_file(self, file_name):
        """Call conjure and return solution as string


        Args:
            file_name (str): name of the file

        Returns:
            str: Emini string of the solution
        """        
        
        params = ""
        conjureCall = ['conjure','solve', file_name]
        subprocess.run(conjureCall, check=True)
        try:
            with open("./conjure-output/model000001-solution000001.solution") as solution:
                s = solution.read()
        except:
            # add error or timeout node or edge
            # add no solution node
            print("error while reading solution")
        return  s
    
    def transform_with_GP2(self,ID, program_name):
        """Transform Emini spec using GP2. The program is compiled automatically if needed

        Args:
            emini_string (str): Emini spec in string format
            program_name (str): name of the program. It should match the name of an existing .gp2 file in the gp2 folder.

        Returns:
            str: Emini string of the transformed spec. If the transformation has no effect or is not applied the input string is return.
        """        
        emini_string = self.graph.nodes[ID]['emini']
        gp2string = self.FormToForm(emini_string,"Emini","GP2String")
        gp2hostfile = "emini_string.host"
        with open(gp2hostfile, 'w') as file:
            file.write(gp2string)

        # check if the compiled program exists, if not compiles program
        if not gp2Interface.is_program_compiled(program_name):
            gp2Interface.compileGP2Program(program_name)
        # Apply Transform
        #hostGraph = os.path.join("gp2",gp2hostfile)
        gp2Interface.runPrecompiledProg(program_name,gp2hostfile)

        gp2_NEWstring = ""
        # If trasform is applicable solve new spec
        if os.path.isfile("gp2.output"):
            with open("gp2.output") as newGP2spec:
                gp2_NEWstring = newGP2spec.read()
            if gp2_NEWstring[:15] == 'No output graph':
                emini_transformed = emini_string # The transform is not applicable

            else:
                emini_transformed = self.FormToForm(gp2_NEWstring,"GP2String","Emini")
              # Clear files
            os.remove("gp2.output")
            
        else:
            print(f"Transform {program_name} not applied")
            emini_transformed = emini_string # The transform has not been applied
        emini_transformed_ID = self.add_e_node(emini_transformed)
        self.add_e_edge(ID,emini_transformed_ID,program_name)

        if os.path.isfile("gp2.log"):
                os.remove("gp2.log")
        os.remove(gp2hostfile)

        return emini_transformed_ID
    
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
    
    def Abstract_to_InstaGen(self,abstract_spec):
        '''
        From abstract spec 
        to instagen spec
        turns Givens into Finds'''
        insta_gen  = instaGen.specToInstaGen(self.FormToForm(abstract_spec,"Emini","ASTpy"))
        return self.FormToForm(insta_gen, "ASTpy","Emini")
    
    def epsilon_greedy_arm_selection(self, rewards):
        if random.random() < self.epsilon:  # Exploration
            chosen_func = random.choice(self.gp2arms)
        else:  # Exploitation
            #pick highest scoring gp2 transformation
            chosen_func = max(rewards.items(), key=lambda trials: trials[1][1])[0]
        return chosen_func

    
    def expand_from_node(self, nodeID, method="multi_armed_bandit"):
        """ Transform the essence spec in a Node using the method provided

        Args:
            nodeID (str): node ID that will be transformed
            method (str): method used. Currently available: "multi_armed_bandit"
        """        
        if method=="multi_armed_bandit":
            # get past arms rewards inside node
            # select an arm using heuristic
            # use arm
            # update rewards based on results

            if "trials" not in self.graph.nodes[nodeID]:
                 # maybe change to defaultdict
                self.graph.nodes[nodeID]["trials"] = {}
                for arm in self.gp2arms:
                    self.graph.nodes[nodeID]["trials"][arm] = [0,0] # 0 number of trials and 0 rewards

            chosen_func = self.epsilon_greedy_arm_selection(self.graph.nodes[nodeID]["trials"])
            new_nodeID = self.transform_with_GP2(nodeID,chosen_func)
            reward = 0 
            if new_nodeID != nodeID:
                reward = 1 # change to some function based on performance
            num_trials, rewards = self.graph.nodes[nodeID]["trials"][chosen_func]
            self.graph.nodes[nodeID]["trials"][chosen_func] = [num_trials+1,rewards+reward]

            # Solve new spec
            solution = []
            if reward > 0:
                solution = self.solve(new_nodeID)
                print("solution ID", solution)
                # add rewards
            


# Transforms: change format, from int sequence (gen), solve, transform with GP2, normalise, transform with ?.
