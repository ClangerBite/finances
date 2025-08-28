from src.file_IO.filepath_utilities import get_filepaths, get_filepath
from src.file_IO.filepath_utilities import get_abs_path
from src.file_IO.read_files import read_json, read_csv_headerless
from src.logging.application_logs import log_debug, log_error, log_output
from src.core.bond_return import test_bond_yield_calcs
from src.file_IO.read_statement import parse_statement


CONFIG_RELATIVE_PATH = 'config/config_sensitive.json' 

COMPONENT_FLAG = 3

  
def run_application():
    
    # Load configuration file
    sensitive = read_json(get_abs_path(CONFIG_RELATIVE_PATH))
    
    # Component - Get list of file paths
    if COMPONENT_FLAG == 1:
   
        files = get_filepaths(sensitive['transaction_dir'])    
        log_output.info(files)        
        log_output.info("\n".join(files))
        
    # Component - Bond yield calcs
    if COMPONENT_FLAG == 2:
        test_bond_yield_calcs()
        
    # Component - Read statements
    if COMPONENT_FLAG == 3:
        filepath = get_filepath (sensitive['statement_dir'], sensitive['statement_file'])
        log_output.info(f"Reading statement file: {filepath}")
        
        data = read_csv_headerless(filepath)
        parse_statement(data)
        
   
        # [next step - read the statement csv file]

    
    




