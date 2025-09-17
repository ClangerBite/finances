from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List


@dataclass
class Statement:
    """Represents the data in an IBKR financial statement"""
    date: str
    account: str
    open_positions: List
    open_accruals: List
    net_asset_values: str
    

@dataclass
class NetAssetValue:
    """Represents the components of Net Asset Value at a given date"""
    NAV_cash: Decimal
    NAV_stock: Decimal
    NAV_options: Decimal
    NAV_bonds: Decimal
    NAV_interest_accruals: Decimal
    NAV_dividend_accruals : Decimal
    total: Decimal = field(init=False)
    
    def __post_init__(self):
        """Convert numeric strings to Decimal objects after initialization"""
        self.NAV_cash = Decimal(str(self.NAV_cash))
        self.NAV_stock = Decimal(str(self.NAV_stock))
        self.NAV_options = Decimal(str(self.NAV_options))
        self.NAV_bonds = Decimal(str(self.NAV_bonds))
        self.NAV_interest_accruals = Decimal(str(self.NAV_interest_accruals))
        self.NAV_dividend_accruals = Decimal(str(self.NAV_dividend_accruals))
        self.total = self.NAV_cash + self.NAV_stock + self.NAV_options + self.NAV_bonds + self.NAV_interest_accruals + self.NAV_dividend_accruals
        
        
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
    gross_amount: Decimal
    net_amount: Decimal
    withholding_tax: Decimal
    amount_per_share: Decimal
    ex_date: datetime
    pay_date: datetime
    currency: str
    unique_ID: str = None

    def __post_init__(self):
        """Convert numeric strings to Decimal objects after initialization"""
        self.quantity = Decimal(str(self.quantity))
        self.gross_amount = Decimal(str(self.gross_amount))
        self.net_amount = Decimal(str(self.net_amount))
        self.withholding_tax = Decimal(str(self.withholding_tax))
        self.amount_per_share = Decimal(str(self.amount_per_share))