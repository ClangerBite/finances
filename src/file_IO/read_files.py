# /////////////////////////////////////////////////////////////////////////////
# UTILITY FUNCTIONS FOR READING FILES 
#
# This module provides a selection of utility functions for reading and parsing
# files in different formats (e.g., YAML, CSV). The functions handle common tasks
# such as opening files, reading their contents, and converting data into usable
# Python structures (e.g., dictionaries, lists).
#
# This module can be re-used across multiple applications, although it is reliant
# on the exceptions defined in the error_handling module.
#
# /////////////////////////////////////////////////////////////////////////////


import csv
import yaml
from typing import List, Dict
from src.monitor import exceptions

  
# ///////////////////////////////////////////////////////////////////////////// 
def read_yaml(abs_path: str) -> Dict:
    """
    Read and parse a YAML file, returning its contents as a dictionary
    
    Args:
        abs_path: Absolute path to the YAML file
    Returns:
        Dictionary containing the parsed YAML data
    """
    
    try:        
        with open(abs_path, 'r') as file:
            parsed_yaml = yaml.safe_load(file)
            
        return parsed_yaml

    except Exception as err:
        raise exceptions.ReadFileError(abs_path, err) 
    

# ///////////////////////////////////////////////////////////////////////////// 
def read_csv_headerless_UTF8(abs_path: str) -> List[List[str]]:
    """
    Read a headerless CSV file encoded in UFT-8 and return the data rows.
    Specifying the encoding as 'utf-8-sig' strips out the UTF-8 Byte Order Mark
    inserted at the start of files downloaded from Interactive Brokers.
    
    Args:
        abs_path: Absolute path to the CSV file
    Returns:
        list of lists representing the data rows
    """
    try:
        with open(abs_path, 'r', encoding='utf-8-sig') as file:
            csv_reader = csv.reader(file)
            return [row for row in csv_reader]  

    except Exception as err:
        raise exceptions.ReadFileError(abs_path, err)