from typing import List, Dict
from datetime import datetime
from core.statements.data_structures import OpenPosition, OpenAccrual, Statement, NetAssetValue
from file_IO.read_files import read_csv_headerless_UTF8
from file_IO.filepaths import get_filepaths
from monitor.log_system import get_loggers
from core.statements.output import output_open_positions_to_browser

# Get logger instances at module level
log_system, log_error, log_output = get_loggers()

  
# /////////////////////////////////////////////////////////////////////////////    
# FUNCTIONS TO READ IBKR STATEMENTS ISAVED LOCALLY IN CSV FORM

def read_statements(statements_directory):
    """Get the list of files in the statements directory and read each in turn"""
    statements = []
    filepaths = get_filepaths(statements_directory)    
    
    for filepath in filepaths:       
        statements.append(read_statement(filepath))

    output_open_positions(statements)
    output_open_accruals(statements)
    output_net_asset_values(statements)
    output_open_positions_to_browser({stmt.account: stmt.open_positions for stmt in statements})
    
    
def read_statement(filepath):
    """Read a statement file, parse it, and store it in a Statement object"""        
    data = read_csv_headerless_UTF8(filepath)
    
    date = get_statement_date(data) 
    account = get_account_number(data)     
    open_positions = get_open_positions(data)
    open_accruals = get_dividend_accruals(data) 
    net_asset_value = get_NAV_data(data)      
    
    return Statement(date, account, open_positions, open_accruals, net_asset_value)


def filter_by_first_item(data, target, index=0):
    """Removes sublists from a list of lists where the first item in the sub-list is not equal to target"""
    return [sublist for sublist in data if sublist and sublist[index] == target]


# /////////////////////////////////////////////////////////////////////////////   
# FUNCTIONS TO GET SPECIFIC INFORMATION FROM STATEMENT DATA

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
   
def get_open_positions(data):    
    """Get the open positions from the Account rows"""
    filtered = filter_by_first_item(data, "Open Positions")
    open_positions = []
    for row in filtered: 
        if row[2] == 'Summary':
            position = OpenPosition(
                ticker=row[5],
                quantity=row[6],
                price=row[10],
                value=row[11],
                currency=row[4]
            )
            open_positions.append(position)
    
    return open_positions

def get_dividend_accruals(data):    
    """Get the open dividend accruals from the Account rows"""
    filtered = filter_by_first_item(data, "Open Dividend Accruals")
    open_accruals = []
    for row in filtered: 
        if row[7] != 'Quantity' and row[7] != '':
            accrual = OpenAccrual(
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
            open_accruals.append(accrual)
    
    return open_accruals


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




        