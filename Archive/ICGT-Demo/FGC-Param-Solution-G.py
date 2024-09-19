import os
import networkx as nx
import matplotlib.pyplot as plt
import k_fold_colouring_to_image
import random

def list_files(directory):
    problem_files = []
    solution_files = []
    for file in os.listdir(directory):
        if file.endswith(".param"):
            problem_files.append(file)
        elif file.endswith(".solution"):
            solution_files.append(file)
    return problem_files, solution_files

def create_file_association_graph(directory):
    problem_files, solution_files = list_files(directory)
    
    G = nx.DiGraph()  # Using a Directed Graph to show the hierarchy and mapping

    # Add a node for the folder and link to all problem files
    folder_node = f"Folder: {os.path.basename(directory)}"
    G.add_node(folder_node, type='folder')

    # Add nodes and edges based on file matches
    for problem_file in problem_files:
        base_name = problem_file[:-6]  # Remove '.param' from the end
        corresponding_solution = f"gcmulti-func-{base_name}.solution"
        
        # Add problem file node and link it to the folder node
        G.add_node(problem_file, type='problem')
        G.add_edge(folder_node, problem_file)

        with open(os.path.join(directory,problem_file)) as f:
                G.nodes[problem_file]['emini'] = f.read()

        # Check if the corresponding solution file exists
        if corresponding_solution in solution_files:
            G.add_node(corresponding_solution, type='solution')
            G.add_edge(problem_file, corresponding_solution)

            with open(os.path.join(directory,corresponding_solution)) as f:
                G.nodes[corresponding_solution]['emini'] = f.read()
            
            #create images
            sol_img_path, inst_img_path = k_fold_colouring_to_image.solution_to_image(os.path.join(directory,problem_file),os.path.join(directory,corresponding_solution))
            G.nodes[corresponding_solution]['image'] = sol_img_path
            G.nodes[problem_file]['image'] = inst_img_path
        elif problem_file[-5:] == "param" and (problem_file[:7] == "gcmulti" or problem_file[:1] == "n"): 
            inst_img_path = k_fold_colouring_to_image.solution_to_image(os.path.join(directory,problem_file))
            G.nodes[problem_file]['image'] = inst_img_path
    return G

directory_path = './tests/gcmulti'
file_graph = create_file_association_graph(directory_path)


from networkx.readwrite import json_graph

data = json_graph.node_link_data(file_graph)
#print("DATA:", data)
import json
s = json.dumps(data)
with open("ICGT-Demo/graphcolourstest3.json", 'w') as file:
        s2 = s.replace("\\n", "    <br/>")
        file.write(s2)