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