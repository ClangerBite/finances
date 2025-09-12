from dataclasses import dataclass
from decimal import Decimal

from typing import List


@dataclass
class Statement:
    """Represents the data in aan IBKR financial statement"""
    date: str
    account: str
    open_positions: List
    open_accruals: List


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
    ex_date: str # Convert to date type
    pay_date: str
    currency: str
    unique_ID: str = None

    def __post_init__(self):
        """Convert numeric strings to Decimal objects after initialization"""
        self.quantity = Decimal(str(self.quantity))
        self.gross_amount = Decimal(str(self.gross_amount))
        self.net_amount = Decimal(str(self.net_amount))
        self.withholding_tax = Decimal(str(self.withholding_tax))
        self.amount_per_share = Decimal(str(self.amount_per_share))