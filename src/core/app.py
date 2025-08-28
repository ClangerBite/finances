from src.file_IO.filepath_utilities import get_filepaths
from src.file_IO.json_utilities import read_json
from src.logging.application_logs import log_debug, log_error, log_output
from src.core.bond_return import test_bond_yield_calcs


  
def run_application():
    
    component_flag = 3
    
    log_output.info("Logging system initialised")    
    sensitive = read_json('config/config_sensitive.json')
    
    # Component - Get list of file paths
    if component_flag == 1:
   
        files = get_filepaths(sensitive['transaction_dir'])    
        log_output.info(files)        
        log_output.info("\n".join(files))
        
    # Component - Bond yield calcs
    if component_flag == 2:
        test_bond_yield_calcs()
    

    

   
    # [next step - read the trade files into a list of trade objects]

    
    




