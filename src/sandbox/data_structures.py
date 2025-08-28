# /////////////////////////////////////////////////////////////////////////////
# © 2023 SUNIL J. PATEL
# VERSION: 1.0.0
#
# This module contains the Data Classes used to store a row of data for each
# separate type of information. All the classes use the @dataclass decorator.
# /////////////////////////////////////////////////////////////////////////////


# IMPORT PACKAGES, MODULES, CLASSES AND CLASS INSTANCES
# /////////////////////////////////////////////////////////////////////////////
from dataclasses import dataclass, field
from datetime import datetime


# FIXME OLD DATA TYPE 
@dataclass(order=True)
class TradeFromDBASE:
    sort_index: str = field(init=False, repr=False)

    tradedate: datetime
    reportdate: datetime
    ticker: str
    originalticker: str
    trantype: str
    quantity: float
    currency: str
    amt_before_costs: float
    costs: float
    amt_after_costs: float
    price: float
    broker: str
    notes: str
    taxable: bool
    tax_year: str
    s104Pool: str
    sortkey: str
    ID: str

    def __post_init__(self) -> None:
        # sort by sort_key
        self.sort_index = self.sortkey
        
# FIXME OLD DATA TYPE
@dataclass(frozen=True)
class AuditedQuantity:
    ticker: str
    statement_quantity: float
    trade_quantity: float
    difference: float
    matched: bool
    
# FIXME OLD DATA TYPE
@dataclass(frozen=True)
class Attributes:
    tradebuy: bool
    tradesell: bool 
    admin: bool
    security: bool
    qtychange: bool
    tradeamount: bool
    tradefee: bool
    shareprice: bool
    





# TRADE DATACLASS - STORES DATA FOR A SINGLE TRANSACTION (PRE-CGT MATCHING)
# /////////////////////////////////////////////////////////////////////////////    
@dataclass
class Trade:
    tradeID: int
    tradedate: datetime
    reportdate: datetime
    ticker: str   
    trantype: str
    quantity: float
    currency: str
    amt_before_costs: float
    costs: float
    amt_after_costs: float
    price: float
    broker: str
    notes: str
    
# STATEMENT DATACLASS - STORES DATA FOR A SINGLE ROW FROM A STATEMENT
# /////////////////////////////////////////////////////////////////////////////    
@dataclass
class Statement:
    statementID: int
    reportdate: datetime
    ticker: str   
    quantity: float
    currency: str
    marketvalue: float
    broker: str
    notes: str

# TICKER DATACLASS - STORES INFORMATION ABOUT A REVISION TO A TICKER CODE
# /////////////////////////////////////////////////////////////////////////////
@dataclass
class Ticker:
    tickerID: int
    original_ticker: str
    revised_ticker: str
    date_changed: datetime
    reason: str

# TRANTYPE DATACLASS - STORES INFORMATION ABOUT A SPECIFIC TRANSACTION TYPE
# /////////////////////////////////////////////////////////////////////////////
@dataclass
class TranType:
    trantypeID: int
    trantype: str
    admin: str
    quantity_change: str
    income: str
    charge: str
    tax: str
    
# FX DATACLASS - STORES A SINGLE FX RATE
# /////////////////////////////////////////////////////////////////////////////
@dataclass
class FX:
    fxID: int
    date: datetime
    currency: str
    fx_rate: float

# BROKERACCOUNT DATACLASS - STORES INFORMATION ABOUT A SINGLE BROKERAGE ACCOUNT
# /////////////////////////////////////////////////////////////////////////////
@dataclass
class BrokerAccount:
    brokerID: int
    broker: str
    name: str
    account_type: str
    tax_status: str
    active_status: str
    date_opened: datetime
    date_closed: datetime