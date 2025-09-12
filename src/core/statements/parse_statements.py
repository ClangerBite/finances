from typing import List, Dict
from datetime import datetime
from core.statements.data_structures import OpenPosition, OpenAccrual, Statement
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
        data = read_csv_headerless_UTF8(filepath)
        date, account, open_positions, open_accruals = parse_statement(data)        
        statements.append(Statement(date, account, open_positions, open_accruals))

    output_open_positions(statements)
    output_open_accruals(statements)
    
    
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
   

def parse_statement(data):
    """Parse the data that has been read from an Open Positions CSV file"""
    
    date = None
    account = None
    nav = None
    open_positions = []
    open_accruals = []    
    
    for row in data:        
        match row[0]:
            case 'Statement':
                if date is None:
                    date = parse_statement_row(row)
                                    
            case 'Account Information':
                if account is None:
                    account = parse_account_information_row(row)
                
            case 'Open Positions':
                valid, position =parse_open_position_row(row)
                if valid:
                    open_positions.append(position)
                    
            case 'Open Dividend Accruals':
                valid, accrual = parse_dividend_accrual_row(row)
                if valid:
                    open_accruals.append(accrual)    

            case 'Net Asset Value':
                pass  # Future implementation
            
            case 'Change in NAV':
                pass  # Future implementation

            case 'Complex Positions Summary':
                pass  # Future implementation
            
            case 'Financial Instrument Information':
                pass  # Future implementation
                
            case 'Base Currency Exchange Rate':
                pass  # Future implementation
            
            case 'Location of Customer Assets, Positions and Money':
                pass  # Future implementation
            
            case _:
                log_error.warning(f"Unknown row type: {row[0]}")
        
    return date, account, open_positions, open_accruals

def parse_statement_row(row):    
    """Get a datetime object date from the string format September 10, 2025"""
    if row[2] != 'Period':
        return None
    dt = datetime.strptime(row[3], "%B %d, %Y")
    return dt.date()

def parse_account_information_row(row):
    return row[3] if row[2] == 'Account' else None

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





        