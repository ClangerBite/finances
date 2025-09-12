from file_IO.filepaths import get_filepaths
from file_IO.filepaths import get_abs_path
from file_IO.read_files import read_yaml, read_csv_headerless_UTF8
from monitor.log_system import get_loggers
from sandbox.yields.bond_return import test_bond_yield_calcs
from core.statements.parse_statements import read_statements


CONFIG_RELATIVE_PATH = 'src/config/config_sensitive.yaml'

COMPONENT_FLAG = 3

  
def run_application():
    """Main application entry point"""
    log_system, log_error, log_output = get_loggers()    
    log_system.info("Logging system initialised")
    
    # Load configuration file
    sensitive = read_yaml(get_abs_path(CONFIG_RELATIVE_PATH))
    
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
        read_statements(sensitive['statement_dir'])
        
        

        
   







