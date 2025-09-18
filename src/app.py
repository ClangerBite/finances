from file_IO.filepaths import get_filepaths
from file_IO.filepaths import get_abs_path
from file_IO.read_files import read_yaml, read_csv_headerless_UTF8
from monitor.log_system import get_loggers
from sandbox.yields.bond_return import test_bond_yield_calcs
from engine.IBKR_statements import process_ibkr_statements_directory
from front_end.output import display_portfolio_pages

# Get logger instances at module level
log_system, log_error, log_output = get_loggers()


CONFIG_RELATIVE_PATH = 'src/config/config_private.yaml'

COMPONENT_FLAG = 3


  
def run_application():
    """Main application entry point"""   
    
    log_system.info("Logging system initialised")
    sensitive = read_yaml(get_abs_path(CONFIG_RELATIVE_PATH))
    log_system.info("Sensitive configurations initialised")
    
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
        statements = process_ibkr_statements_directory(sensitive['statement_dir'])
        
        output_open_positions(statements)
        output_open_accruals(statements)
        output_net_asset_values(statements)
                                    
        display_portfolio_pages(
            {stmt.account: stmt.open_positions for stmt in statements},
            {stmt.account: stmt.open_accruals for stmt in statements}
    )
        
        
# /////////////////////////////////////////////////////////////////////////////   
# FUNCTIONS TO OUTPUT STATEMENT INFORMATION TO LOGS

def output_open_positions(statements):
    for statement in statements:
        log_output.info(f"OPEN POSITIONS IN ACCOUNT {statement.account} AS AT {statement.date}:")  
        for item in statement.open_positions: 
            log_output.info(item)

def output_open_accruals(statements):
    for statement in statements:
        log_output.info(f"OPEN ACCRUALS IN ACCOUNT {statement.account} AS AT {statement.date}:") 
        for item in statement.open_accruals: 
            log_output.info(item)
            
def output_net_asset_values(statements):
    for statement in statements:
        log_output.info(f"NAV FOR ACCOUNT {statement.account} AS AT {statement.date}:") 
        log_output.info(f"Cash = {statement.net_asset_values.NAV_cash}")  
        log_output.info(f"Stock = {statement.net_asset_values.NAV_stock}")
        log_output.info(f"Options = {statement.net_asset_values.NAV_options}")
        log_output.info(f"Bonds = {statement.net_asset_values.NAV_bonds}")
        log_output.info(f"Interest Accruals = {statement.net_asset_values.NAV_interest_accruals}")
        log_output.info(f"Dividend Accruals = {statement.net_asset_values.NAV_dividend_accruals}")
        log_output.info(f"TOTAL = {statement.net_asset_values.total}")

        
   







