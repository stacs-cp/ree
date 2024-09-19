import os
import glob
from collections import defaultdict
import sys
sys.path.append('.')
from greee import eminipyparser
from greee import essence_transforms
import networkx as nx
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer
import umap

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
            
            total_essence += len(essence_files)
            total_param += len(param_files)
    
    return result, total_essence, total_param

def check_parsable_essence_files(root_folder):
    folder_analysis, total_essence, total_param = catalogue_to_dict(root_folder)
    results = defaultdict(dict)
    error_count = 0

    # Load sentence transformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    # UMAP for dimensionality reduction
    reducer = umap.UMAP(n_neighbors=15, n_components=2, metric='euclidean')

    for folder, files in folder_analysis.items():
        essence_texts = []
        for essence_file in files['essence']:
            try:
                with open(essence_file, 'r') as file:
                    raw_string = file.read()
                
                parser = eminipyparser.EssenceParser()
                statements = parser.parse(raw_string)
                essence_texts.append(raw_string)
                
                results[folder][essence_file] = {
                    'emini': raw_string,
                    'error': ""
                }
            except Exception as e:
                error_count += 1
                results[folder][essence_file] = {
                    'emini': raw_string,
                    'error': str(e)
                }
                print(f"Error processing file {essence_file}: {str(e)}")
                print(f"Total errors: {error_count}")

        # Generate embeddings and apply UMAP
    if essence_texts:
        embeddings = model.encode(essence_texts)
        reduced_data = reducer.fit_transform(embeddings)
        print(reduced_data)
        # Store the 2D points
        for i, essence_file in enumerate(files['essence']):
            results[folder][essence_file]['x'] = reduced_data[i, 0]
            results[folder][essence_file]['y'] = reduced_data[i, 1]

    return results, total_essence, total_param

def transform_catalogue(catalogue_path):
    specs_dict, specs_num, param_num = check_parsable_essence_files(catalogue_path)

    print("____________")
    print(specs_dict)
    et = essence_transforms.EssenceTransforms()
    for folder, file_results in specs_dict.items():
        print(f"\nFolder: {folder}")
        for file, result in file_results.items():
            if result['error'] == '':
                print(f"  File: {file}")
                print(f"  x: {result['x']}, y: {result['y']}")

if __name__ == "__main__":
    catalogue_path = '/Users/cls29/EssenceCatalog/problems'
    transform_catalogue(catalogue_path)
