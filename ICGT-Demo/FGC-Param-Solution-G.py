import os
import networkx as nx
import matplotlib.pyplot as plt
import k_fold_colouring_to_image

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

        # Check if the corresponding solution file exists
        if corresponding_solution in solution_files:
            G.add_node(corresponding_solution, type='solution')
            G.add_edge(problem_file, corresponding_solution)
            #create images
            sol_img_path, inst_img_path = k_fold_colouring_to_image.solution_to_image(os.path.join(directory,corresponding_solution), os.path.join(directory,problem_file))
            G.nodes[corresponding_solution]['image'] = sol_img_path
            G.nodes[problem_file]['image'] = inst_img_path
    return G

# Replace 'your_directory_path' with the path to the directory containing your files
directory_path = '/Users/cls29/ree/tests'
file_graph = create_file_association_graph(directory_path)

# Print the nodes and edges to verify the graph
#print("Nodes:", file_graph.nodes(data=True))
#print("Edges:", list(file_graph.edges))

#nx.draw(file_graph,pos=nx.fruchterman_reingold_layout(file_graph), node_size=5)
#plt.show()

from networkx.readwrite import json_graph

data = json_graph.node_link_data(file_graph)
print("DATA:", data)
import json
s = json.dumps(data)
with open("ICGT-Demo/graphcolourstest2.json", 'w') as file:
        s2 = s.replace("\\n", "<br/>")
        file.write(s2)