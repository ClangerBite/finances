import json
from src.file_IO.filepath_utilities import get_abs_path
from src.error_handling import exceptions

  
# ///////////////////////////////////////////////////////////////////////////// 
def read_json(relative_path):
    """Read and parse a JSON file, returning its contents as a dictionary"""
    
    abs_path = get_abs_path(relative_path)
    
    try:        
        with open(abs_path) as file:
            parsed_json = json.load(file)
        
        return parsed_json

    except Exception as err:
        raise exceptions.ReadFileError(abs_path, err) 