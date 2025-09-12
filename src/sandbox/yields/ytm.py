from datetime import date
from typing import List, Tuple
import numpy as np
from src.monitor.log_system import get_loggers

# Get logger instances at module level
log_system, log_error, log_output = get_loggers()


def calculate_ytm(
    purchase_price: float,
    purchase_date: date,
    par_value: float,
    cash_flows: List[Tuple[date, float]],
    maturity_date: date,
    guess: float = 0.05,  # Initial guess of 5%
    tolerance: float = 0.0001
) -> float:
    """
    Calculate yield to maturity using Newton-Raphson method
    
    Args:
        purchase_price: Bond purchase price
        purchase_date: Date of purchase
        par_value: Par value of bond
        cash_flows: List of tuples containing (payment_date, payment_amount)
        maturity_date: Bond maturity date
        guess: Initial YTM guess (default 5%)
        tolerance: Acceptable error margin
        
    Returns:
        float: Yield to maturity as a decimal (e.g., 0.05 for 5%)
    """
    log_system.debug(f"Calculating YTM for bond purchased at {purchase_price}")
    
    
    
    # def get_years_to_payment(payment_date: date) -> float:
    #     """Calculate fractional years between purchase date and payment date"""
    #     days = (payment_date - purchase_date).days
    #     return days / 365.0
    
    
    
    def get_years_to_payment(payment_date: date) -> float:
        """
        Calculate fractional years between purchase date and payment date using 30/360 convention
        
        The 30/360 convention:
        - Assumes 30 days per month
        - Assumes 360 days per year
        - Formula: (Y2-Y1) * 360 + (M2-M1) * 30 + (D2-D1)) / 360
        where Y=year, M=month, D=day
        """
        y1, m1, d1 = purchase_date.year, purchase_date.month, purchase_date.day
        y2, m2, d2 = payment_date.year, payment_date.month, payment_date.day
        
        # Adjust for end of month cases
        if d1 == 31:
            d1 = 30
        if d2 == 31 and d1 >= 30:
            d2 = 30
            
        days = ((y2 - y1) * 360) + ((m2 - m1) * 30) + (d2 - d1)
        return days / 360.0
    
    
    
    

    def present_value(rate: float) -> float:
        """Calculate present value of all cash flows at given rate"""
        pv = 0
        for payment_date, amount in cash_flows:
            years = get_years_to_payment(payment_date)
            pv += amount / ((1 + rate) ** years)
        
        # Add present value of par amount at maturity
        years_to_maturity = get_years_to_payment(maturity_date)
        pv += par_value / ((1 + rate) ** years_to_maturity)
        return pv

    def pv_derivative(rate: float) -> float:
        """Calculate derivative of present value function"""
        derivative = 0
        for payment_date, amount in cash_flows:
            years = get_years_to_payment(payment_date)
            derivative -= years * amount / ((1 + rate) ** (years + 1))
            
        years_to_maturity = get_years_to_payment(maturity_date)
        derivative -= years_to_maturity * par_value / ((1 + rate) ** (years_to_maturity + 1))
        return derivative

    # Newton-Raphson iteration
    rate = guess
    for _ in range(100):  # Maximum iterations
        try:
            pv = present_value(rate)
            difference = pv - purchase_price
            
            if abs(difference) < tolerance:
                log_system.info(f"YTM calculation converged at {rate:.4%}")
                return rate
                
            derivative = pv_derivative(rate)
            rate = rate - difference / derivative
            
        except ZeroDivisionError:
            log_error.error("YTM calculation failed - division by zero")
            return None
            
    log_error.warning("YTM calculation did not converge")
    return None

# Example usage:
if __name__ == "__main__":
    # Test data
    test_cash_flows = [
        (date(2024, 1, 30), 0.71875),  # Quarterly payments of $0.71875 (2.875% annual)
        (date(2024, 4, 30), 0.71875),
        (date(2024, 7, 30), 0.71875),
        (date(2024, 10, 30), 0.71875)
    ]
    
    ytm = calculate_ytm(
        purchase_price=24.50,
        purchase_date=date.today(),
        par_value=25.00,
        cash_flows=test_cash_flows,
        maturity_date=date(2026, 2, 15)
    )
    
    if ytm:
        print(f"Yield to Maturity: {ytm:.2%}")
        
        
        
        
# I'll help create a function to calculate the Yield to Maturity (YTM) using the Newton-Raphson method, since YTM must be solved iteratively. Here's the implementation:

# The above implementation:

# Uses Newton-Raphson method for iterative approximation
# Handles both regular interest payments and final par value repayment
# Accounts for time value of money using actual day count
# Includes error handling and logging
# Provides progress information via debug logging
# Returns YTM as a decimal (e.g., 0.05 for 5%)

# Key features:

# Type hints for better code maintenance
# Nested functions for cleaner scope management
# Error handling for division by zero and non-convergence
# Logging for debugging and error tracking
# Configurable tolerance and initial guess
# Day count based on actual/365 convention





# Example integration with existing code
def calculate_bond_ytm(security: dict) -> float:
    cash_flows = [(date, security['par'] * security['coupon'] / security['frequency']) 
                  for date, _ in dividend_dates_to_maturity]
    
    return calculate_ytm(
        purchase_price=security['current_price'],
        purchase_date=date.today(),
        par_value=security['par'],
        cash_flows=cash_flows,
        maturity_date=security['maturity']
    )