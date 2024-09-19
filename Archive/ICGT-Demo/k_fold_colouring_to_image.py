import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.colors import LinearSegmentedColormap, ListedColormap

from PIL import Image, ImageDraw
import re
import os

def parse_graph_file(file_path):
    graph_data = {}
    with open(file_path, 'r') as file:
        for line in file:
            if 'letting n be' in line:
                graph_data['n'] = int(re.findall(r'letting n be (\d+)', line)[0])
            elif 'letting edges be relation' in line:
                edges_text = re.findall(r'relation\((.+)\)', line)[0]
                graph_data['edges'] = eval(f'[{edges_text}]')
            elif 'letting numberColours be' in line:
                graph_data['numberColours'] = int(re.findall(r'letting numberColours be (\d+)', line)[0])
            elif 'letting coloursPerNode be' in line:
                graph_data['coloursPerNode'] = int(re.findall(r'letting coloursPerNode be (\d+)', line)[0])
    
    return create_graph(graph_data)

def create_graph(graph_data):
    G = nx.Graph()
    G.add_nodes_from(range(graph_data['n']))
    G.add_edges_from(graph_data['edges'])
    return G


def solution_to_image(instance, solution_path = None):
    
    imgtype = ".png"
    G = nx.Graph()
   
    if "dodecah" in instance:
        G = nx.dodecahedral_graph()
        # Generate initial positions
        positions = generate_positions(d1, d2)

        # Define the custom node orders
        outer_nodes = [0, 10, 9, 13, 14, 15, 5, 4, 3, 19]
        inner_nodes = [1, 11, 8, 12, 7, 16, 6, 17, 2, 18]
        custom_positions = assign_custom_names(positions, outer_nodes, inner_nodes)
    else:
        
        G = parse_graph_file(instance)
        custom_positions = nx.spring_layout(G)
        
    if solution_path == None:
        nx.draw(G, node_size = 400)
    
        plt.ylim(-1.3,1.3)
        plt.xlim(-1.3,1.3)
        #plt.tight_layout()
        inst_name = f"{os.path.split(instance)[-1]}.png"
        instance_image_path = os.path.join("ICGT-Demo","imgs",inst_name )
        plt.savefig(instance_image_path)
        #plt.savefig(f"zzinst.png",bbox_inches='tight')
        plt.close()
        create_circular_image(instance_image_path)
        return os.path.join("imgs", inst_name)

    with open(solution_path) as file:
        solution = file.read()
    
    pattern = r'function(\(.*?\))'
    # Search for the pattern in the text
    match = re.search(pattern, solution, re.DOTALL)
    # If a match is found, return the content within the parentheses
    s = match.group(1).split("},")
    s2 = {}
    for substring in s:
        pair = substring.replace("(","").replace("{","").replace("}","").replace(")","").replace("\n","").split("-->")
        colours = pair[1].split(",")
        s2[int(pair[0])] = [int(c) for c in colours]


    # parameters for pie plot
    radius = 0.0715
    cmap = plt.cm.viridis

    n_colours = 25
    # storing attributes in a dict

    attrs = s2

    # Create a color palette for the unique integers
    color_palette = generate_color_palette(n_colours)

    # Map your integer sequence to the colors
    mapped_colors = []
    for nodecolours in s2:
        colours_in_node = []
        for c in s2[nodecolours]:
            colours_in_node.append(color_palette[c-1])
        mapped_colors.append(colours_in_node)

    # Specify the distances
    d1 = 0.6
    d2 = 0.99

    # Assign custom names to the positions

    radius = 0.07
    cmap = plt.cm.viridis
    nx.draw_networkx_edges(G, pos=custom_positions)
    for node in G.nodes:

        attributes = attrs[node]

        plt.pie(
            [1]*len(attributes), # s.t. all wedges have equal size
            center=custom_positions[node],
            colors = mapped_colors[node],
            wedgeprops={"edgecolor":"k",'linewidth': 0.5, 'antialiased': True},
            radius=radius)

 
    plt.ylim(-1,1)
    plt.xlim(-1,1)
    plt.tight_layout()
    
    sol_name = f"{os.path.split(solution_path)[-1]}{imgtype}"
    solution_image_path = os.path.join("ICGT-Demo","imgs", sol_name)
    plt.savefig(solution_image_path)
    #plt.savefig(f"zzsol.png",bbox_inches='tight')
    plt.close()
    nx.draw(G,pos=custom_positions, node_size = 400)
    
    plt.ylim(-1.1,1.1)
    plt.xlim(-1.1,1.1)
    #plt.tight_layout()
    inst_name = f"{os.path.split(instance)[-1]}{imgtype}"
    instance_image_path = os.path.join("ICGT-Demo","imgs",inst_name )
    plt.savefig(instance_image_path)
    #plt.savefig(f"zzinst.png",bbox_inches='tight')
    plt.close()
    return os.path.join("imgs", sol_name), os.path.join("imgs", inst_name)



def create_circular_image(image_path):
    # Load the original image and convert it to 'RGBA' for transparency support
    img = Image.open(image_path).convert("RGBA")
    
    # Create a mask image with the same dimensions as the original image, but fully opaque
    mask = Image.new('L', img.size, 0)
    
    # Create a draw object to draw on the mask image
    draw = ImageDraw.Draw(mask)
    
    # Calculate the center and the radius for the circle
    center_x, center_y = img.size[0] // 2, img.size[1] // 2
    radius = min(center_x, center_y)  # Radius is set to fit within the image
    
    # Draw a white (opaque) circle in the center of the mask
    draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), fill=255)
    
    # Apply the mask as an alpha channel to the original image
    img.putalpha(mask)
    
    # Create a new image with transparent background and same size as original
    transparent_img = Image.new('RGBA', img.size, (0, 0, 0, 0))  # Transparent image
    
    # Paste the original image onto the transparent background using the mask
    transparent_img.paste(img, (0, 0), mask=img)
    
    # Save or display the result
    transparent_img.save(image_path)
    #transparent_img.show()

    # Usage
    #create_circular_image(image_path)

def generate_positions(d1, d2):
        positions = {}
        angles = np.linspace(0, 2 * np.pi, 10, endpoint=False)  # Generate 10 angles evenly spaced around the circle

        # Place 10 nodes at distance d1
        for i, angle in enumerate(angles):
            x = d1 * np.cos(angle)
            y = d1 * np.sin(angle)
            positions[i] = (x, y)

        # Place another 10 nodes at distance d2, using the same angles
        for i, angle in enumerate(angles):
            x = d2 * np.cos(angle)
            y = d2 * np.sin(angle)
            positions[i + 10] = (x, y)  # Offset the node indices by 10

        return positions

def assign_custom_names(positions, outer_nodes, inner_nodes):
        new_positions = {}

        # First handle the outer circle nodes
        for new_node, old_node in zip(outer_nodes, range(10, 20)):
            new_positions[new_node] = positions[old_node]

        # Now handle the inner circle nodes
        for new_node, old_node in zip(inner_nodes, range(10)):
            new_positions[new_node] = positions[old_node]

        return new_positions

def generate_color_palette(n):
    cmap = plt.get_cmap('gist_rainbow')  
    colors = [cmap(i/n) for i in range(n)]
    return colors

if __name__ == "__main__":
    solutionfile = ""
    paramfile = ""

    solution_to_image(paramfile,solutionfile)