import json

def is_json_valid(file_path):
    try:
        with open(file_path, 'r') as file:
            json.load(file)  # Try loading the file with json module
        print(f"The JSON file '{file_path}' is valid.")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON file '{file_path}': {e}")
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
file_path = '/Users/cls29/ree/experiments/graphcolourstest2.json'
is_json_valid(file_path)
