import json

def load_json(file_path):
    """
    Load JSON data from a file.

    Parameters:
    - file_path (str): The path to the JSON file.

    Returns:
    - dict: A Python dictionary representing the JSON data.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file '{file_path}': {e}")
        return None


