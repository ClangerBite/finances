import csv
import json
from typing import List, Dict
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
    

# ///////////////////////////////////////////////////////////////////////////// 
def read_csv_headerless(abs_path: str) -> List[List[str]]:
    """
    Read a headerless CSV file and return the data rows
    
    Args:
        abs_path: Absolute path to the CSV file
    Returns:
        list of lists representing the data rows
    """
    try:
        with open(abs_path, 'r') as file:
            csv_reader = csv.reader(file)
            return [row for row in csv_reader]  

    except Exception as err:
        raise exceptions.ReadFileError(abs_path, err)