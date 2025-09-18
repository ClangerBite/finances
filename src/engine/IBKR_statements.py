from typing import List
from datetime import datetime
from engine.data_structures import OpenPosition, OpenAccrual, Statement, NetAssetValue
from file_IO.read_files import read_csv_headerless_UTF8
from file_IO.filepaths import get_filepaths

  
# /////////////////////////////////////////////////////////////////////////////    
# FUNCTIONS TO READ IBKR STATEMENTS ISAVED LOCALLY IN CSV FORM

def process_ibkr_statements_directory(statements_directory: str) -> List[Statement]:
    """Process all IBKR statement files in the given directory and subdirectories
    
    Args:
        statements_directory: Path to parent directory containing IBKR statement files
    Returns:
        List of parsed Statement objects
    """
    statements = []
    filepaths = get_filepaths(statements_directory)    
    
    for filepath in filepaths:       
        statements.append(parse_ibkr_statement(filepath))

    return statements
    
    
def parse_ibkr_statement(filepath: str) -> Statement:
    """Parse an IBKR statement file and extract statement data into a Statement object"""        
    data = read_csv_headerless_UTF8(filepath)
    
    date = get_statement_date(data) 
    account = get_account_number(data)     
    open_positions = get_open_positions(data)
    open_accruals = get_dividend_accruals(data) 
    net_asset_value = get_NAV_data(data)      
    
    return Statement(date, account, open_positions, open_accruals, net_asset_value)


def filter_list_of_lists(data, target, index=0):
    """Removes sublists from a list of lists where the first item in the sub-list is not equal to target"""
    return [sublist for sublist in data if sublist and sublist[index] == target]


# /////////////////////////////////////////////////////////////////////////////   
# FUNCTIONS TO GET SPECIFIC INFORMATION FROM THE STATEMENT DATA READ FROM CSV FILES

def get_account_number(data: List[List[str]]) -> str:    
    """Get the Account number from the Account rows"""
    filtered = filter_list_of_lists(data, "Account Information")
    for row in filtered: 
        if row[2] == 'Account':
            return row[3]


def get_statement_date(data: List[List[str]]) -> datetime:    
    """Get a datetime date from the Statement rows (string format September 10, 2025)"""
    filtered = filter_list_of_lists(data, "Statement")
    for row in filtered: 
        if row[2] == 'Period':
            return datetime.strptime(row[3], "%B %d, %Y")


def get_NAV_data(data: List[List[str]]) -> NetAssetValue:
    """Construct a NetAssetValue object from the Net Asset Value rows"""
    filtered = filter_list_of_lists(data, "Net Asset Value")
    
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
   
   
def get_open_positions(data: List[List[str]]) -> List[OpenPosition]:    
    """Get the open positions from the Account rows"""
    filtered = filter_list_of_lists(data, "Open Positions")
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


def get_dividend_accruals(data: List[List[str]]) -> List[OpenAccrual]:    
    """Get the open dividend accruals from the Account rows"""
    filtered = filter_list_of_lists(data, "Open Dividend Accruals")
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
                ex_date=datetime.strptime(row[5], '%Y-%m-%d'),
                pay_date=datetime.strptime(row[6], '%Y-%m-%d'),
                currency=row[3],         
            )
            open_accruals.append(accrual)
    
    return open_accruals
