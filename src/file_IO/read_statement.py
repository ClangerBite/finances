from src.error_handling import exceptions
from src.logging.application_logs import log_error, log_output
from typing import List, Dict

  
# /////////////////////////////////////////////////////////////////////////////    
   

def parse_statement(data: List[List[str]]) -> List[Dict]:
    """
    Parse CSV data into list of dictionaries
    
    Args:
        data: List of lists of data rows
    Returns:
        List of dictionaries with header fields as keys
    """
    
    date = None
    account = None
    nav = None
    open_pos = {}
    open_accruals = {}
    
    
    for row in data:
        
        match row[0]:
            case 'Statement':
                if date is None:
                    date = parse_statement_row(date, row)
                
            case 'Account Information':
                account = parse_account_information(account, row) 
                if account not in open_pos:
                    open_pos[account] = []
                if account not in open_accruals:
                    open_accruals[account] = []
                
            case 'Open Positions':
                valid, position = add_open_position(row)
                if valid:
                    open_pos[account].append(position)
                    
            case 'Open Dividend Accruals':
                valid, accrual = add_div_accrual(row)
                if valid:
                    open_accruals[account].append(accrual)    

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
        

        log_output.info(f"Parsed row: {row}")
        
    return date, open_pos, open_accruals


def parse_statement_row(date, row):
    if row[2] == 'Period':
        date = row[3]
    return date

def parse_account_information(account, row):
    if row[2] == 'Account':
        account = row[3]
    return account


def add_open_position(row):    
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


def add_div_accrual(row):    
    if row[7] != 'Quantity' and row[7] != '':
    
        return True, OpenAccrual(
            ticker=row[4],
            quantity=row[7],
            gross=row[11],
            net=row[12],
            wht=row[8],
            per_share=row[10],
            ex_date=row[5],
            pay_date=row[6],
            currency=row[3],         
        )
    else:
        return False, None









from dataclasses import dataclass
from decimal import Decimal


@dataclass
class OpenPosition:
    """Represents an open position in a financial instrument"""
    ticker: str
    quantity: Decimal
    price: Decimal
    value: Decimal
    currency: str
    unique_ID: str = None

    def __post_init__(self):
        """Convert numeric strings to Decimal objects after initialization"""
        self.quantity = Decimal(str(self.quantity))
        self.price = Decimal(str(self.price))
        self.value = Decimal(str(self.value))
        

@dataclass
class OpenAccrual:
    """Represents an open dividend accrual in a financial instrument"""
    ticker: str
    quantity: Decimal
    gross: Decimal
    net: Decimal
    wht: Decimal
    per_share: Decimal
    ex_date: str # Convert to date type
    pay_date: str
    currency: str
    unique_ID: str = None

    def __post_init__(self):
        """Convert numeric strings to Decimal objects after initialization"""
        self.quantity = Decimal(str(self.quantity))
        self.gross = Decimal(str(self.gross))
        self.wht = Decimal(str(self.wht))
        self.per_share = Decimal(str(self.per_share))
        self.net = Decimal(str(self.net))
        