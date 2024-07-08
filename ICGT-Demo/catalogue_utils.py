import os
import glob
from collections import defaultdict
import sys
sys.path.append('.')
from greee import eminipyparser

from greee import essence_transforms
import networkx as nx
import matplotlib.pyplot as plt

catalogue_path = '/Users/cls29/EssenceCatalog/problems'

def catalogue_to_dict(root_path):
    '''
    Searches Essence files and Param files and places them into a dict
    '''
    result = {}
    total_essence = 0
    total_param = 0
    
    # Get all immediate subdirectories
    subdirs = [d for d in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, d))]
    
    for subdir in subdirs:
        subdir_path = os.path.join(root_path, subdir)
        
        # Find all .essence files
        essence_files = glob.glob(os.path.join(subdir_path, '**', '*.essence'), recursive=True)
        
        # Only proceed if .essence files are found
        if essence_files:
            # Find all .param files
            param_files = glob.glob(os.path.join(subdir_path, '**', '*.param'), recursive=True)
            
            # Add to result dictionary
            result[subdir] = {
                'essence': essence_files,
                'param': param_files
            }
            
            # Update totals
            total_essence += len(essence_files)
            total_param += len(param_files)
    
    return result, total_essence, total_param

def check_parsable_essence_files(root_folder):
    # Run the analysis from the previous script
    folder_analysis, total_essence, total_param = catalogue_to_dict(root_folder)

    results = defaultdict(list)
    error_count = 0

    for folder, files in folder_analysis.items():
        for essence_file in files['essence']:
            try:
                with open(essence_file, 'r') as file:
                    raw_string = file.read()
                
                parser = eminipyparser.EssenceParser()
                # Parse the raw string
                statements = parser.parse(raw_string)
                
                # Store the results
                results[folder].append({
                    'file': essence_file,
                    'statements': raw_string
                })
            except Exception as e:
                error_count += 1
                print(f"Error processing file {essence_file}: {str(e)}")
                print(f"Total errors: {error_count}")

    return results, total_essence, total_param

def transform_catalogue(catalogue_path):
    specs_dict, specs_num, param_num =  check_parsable_essence_files(catalogue_path)

    print("____________")
    print(specs_dict)

    for folder, file_results in specs_dict.items():
            print(f"\nFolder: {folder}")
            for result in file_results:
                print(f"  File: {result['file']}")
                print(f"  Statements: {result['statements']}")
                print()

                et = essence_transforms.EssenceTransforms()


                spec_ID = et.add_e_node(result['statements'],"StartSpec.essence")
                #solution = etransform_graph.solve(spec_ID)
                #solveTime =time.time_ns() - start
                #parentSolutionID = hash(solution)

                for _ in range(0,30):
                    try: 
                        et.expand_from_node(spec_ID)
                    except Exception as e:
                        print(f"Error processing file {result['file']}: {str(e)}")
                        
                print(et.graph.nodes(data=True))
                pos = nx.spectral_layout(et.graph)
                nx.draw(et.graph, pos)
                node_labels = nx.get_node_attributes(et.graph,'file_name')
                nx.draw_networkx_labels(et.graph, pos, node_labels)
                edge_labels = dict([((n1, n2), d['transformation']) for n1, n2, d in et.graph.edges(data=True)])
                nx.draw_networkx_edge_labels(et.graph, pos, edge_labels=edge_labels)
                plt.show(block=True)
