from typing import List, Dict
from datetime import datetime
from core.statements.data_structures import OpenPosition, OpenAccrual, Statement, NetAssetValue
from file_IO.read_files import read_csv_headerless_UTF8
from file_IO.filepaths import get_filepaths
from monitor.log_system import get_loggers

# Get logger instances at module level
log_system, log_error, log_output = get_loggers()
  
# /////////////////////////////////////////////////////////////////////////////    


def read_statements(statements_directory):
    """Get the list of files in the statements directory and read each in turn"""
    statements = []
    filepaths = get_filepaths(statements_directory)    
    
    for filepath in filepaths:       
        statements.append(read_statement(filepath))

    output_open_positions(statements)
    output_open_accruals(statements)
    output_net_asset_values(statements)
    
    
def read_statement(filepath):
    """Read a statement file, parse it, and store it in a Statement object"""        
    data = read_csv_headerless_UTF8(filepath)
    
    date = get_statement_date(data) 
    account = get_account_number(data)     
    open_positions, open_accruals = parse_raw_statement(data) 

    net_asset_value = get_NAV_data(data)      
    return Statement(date, account, open_positions, open_accruals, net_asset_value)


def filter_by_first_item(data, target):
    """Removes sublists from a list of lists where the first item in the sub-list is not equal to target"""
    return [sublist for sublist in data if sublist and sublist[0] == target]


def get_account_number(data):    
    """Get the Account number from the Account rows"""
    filtered = filter_by_first_item(data, "Account Information")
    for row in filtered: 
        if row[2] == 'Account':
            return row[3]


def get_statement_date(data):    
    """Get a datetime date from the Statement rows (string format September 10, 2025)"""
    filtered = filter_by_first_item(data, "Statement")
    for row in filtered: 
        if row[2] == 'Period':
            dt = datetime.strptime(row[3], "%B %d, %Y")
            return dt.date()


def get_NAV_data(data):
    """Construct a NetAssetValue object from the Net Asset Value rows"""
    filtered = filter_by_first_item(data, "Net Asset Value")
    
    NAV_cash = 0
    NAV_stock = 0
    NAV_options = 0
    NAV_bonds = 0
    NAV_interest_accruals = 0
    NAV_dividend_accruals = 0
        
    for row in filtered:        
        match row[2].rstrip():
            case 'Cash':
                NAV_cash = row[6]
            case 'Stock':
                NAV_stock = row[6]
            case 'Options':
                NAV_options = row[6]
            case 'Bonds':
                NAV_bonds = row[6]
            case 'Interest Accruals':
                NAV_interest_accruals = row[6]
            case 'Dividend Accruals':
                NAV_dividend_accruals = row[6]           
                
    return NetAssetValue(
        NAV_cash,
        NAV_stock,
        NAV_options,
        NAV_bonds,
        NAV_interest_accruals,
        NAV_dividend_accruals
        )



    
    
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
   
   
   

def parse_raw_statement(data):
    """Parse the data that has been read from an Open Positions CSV file"""
    
    date = None
    account = None
    nav = None
    open_positions = []
    open_accruals = []    
    
    for row in data:        
        match row[0]:
            case 'Statement':
                pass
                                    
            case 'Account Information':
                pass
                
            case 'Open Positions':
                valid, position =parse_open_position_row(row)
                if valid:
                    open_positions.append(position)
                    
            case 'Open Dividend Accruals':
                valid, accrual = parse_dividend_accrual_row(row)
                if valid:
                    open_accruals.append(accrual)    

            case 'Net Asset Value':
                pass
            
            case 'Change in NAV':
                pass  # Future implementation

            case 'Complex Positions Summary':
                pass  # Future implementation
            
            case 'Financial Instrument Information':
                pass
                
            case 'Base Currency Exchange Rate':
                pass  # Future implementation
            
            case 'Location of Customer Assets, Positions and Money':
                pass
            
            case _:
                log_error.warning(f"Unknown row type: {row[0]}")
        
    return open_positions, open_accruals

def parse_open_position_row(row):    
    if row[2] == 'Summary':
    
        return True, OpenPosition(
            ticker=row[5],
            quantity=row[6],
            price=row[10],
            value=row[11],
            currency=row[4]
        )
    else:
        return False, None

def parse_dividend_accrual_row(row):    
    if row[7] != 'Quantity' and row[7] != '':
    
        return True, OpenAccrual(
            ticker=row[4],
            quantity=row[7],
            gross_amount=row[11],
            net_amount=row[12],
            withholding_tax=row[8],
            amount_per_share=row[10],
            ex_date=row[5],
            pay_date=row[6],
            currency=row[3],         
        )
    else:
        return False, None





        