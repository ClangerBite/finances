from datetime import date
from monitor.log_system import get_loggers

# Get logger instances at module level
log_system, log_error, log_output = get_loggers()


# Create list of future dividend dates
def generate_dividend_dates(regular_dates, end_date):
    if not end_date:
        log_output.warning("NO MATURITY")
        return

    regular_date_list = append_regular_dates(regular_dates, end_date)
    final_date_list = append_final_date(regular_date_list, end_date)
    return final_date_list


# Generate list of future regular dividend dates
def append_regular_dates(regular_dates, end_date):    
    start_year = date.today().year
    end_year = end_date.year
    date_tupples = []
    
    for year in range(start_year, end_year + 1):
        for regular_date in regular_dates:
            tmp_ex_div_date = date(year,regular_date[0].month, regular_date[0].day)
            tmp_payment_date = date(year,regular_date[1].month, regular_date[1].day)
            tmp_tupple = (tmp_ex_div_date, tmp_payment_date)
            
            if tmp_ex_div_date > date.today() and tmp_ex_div_date <= end_date:
                date_tupples.append(tmp_tupple)
    return date_tupples


# Add irregular final dividend date if appropriate
def append_final_date(date_tupples, end_date):
    if date_tupples[-1][0] != end_date:
        date_tupples.append((end_date, end_date))
    return date_tupples
    

# Convert datetime object to a string object
def date_as_string(date):
    return date.isoformat()


def test_bond_yield_calcs():
    # TEST DATA & FUNCTION CALLS
    security = {
        'ticker': 'RCC',
        'underlying_ticker': 'RC',
        'underlying': 'Ready Capital Corp',
        'type': 'fixed',
        'par': 25,
        'currency': 'US$',
        'coupon': 0.0575,
        'frequency': 4,
        'maturity': date(2026, 2, 15),
        'first_call': date(2025, 4, 30),
        'set_call_dates': False,
        'call_notice_period': 30,
        'current_price': 24.5,
        'ex_div_dates': [date(1000, 1, 14),date(1000, 4, 14), date(1000, 7, 14), date(1000, 10, 14)],
        'payment_dates': [date(1000, 1, 30),date(1000, 4, 30), date(1000, 7, 30), date(1000, 10, 30)]    
    }

    regular_dividend_dates = list(zip(security['ex_div_dates'], security['payment_dates']))

    dividend_dates_to_maturity = generate_dividend_dates(regular_dividend_dates, security['maturity'])

    # Need a function to check if first call date has passed - if so, is there another set date or is it 30 days from today?
    # Are there special terms for early calls (eg 105% of par)?


    # Note - use ex-div dates to create the list of future dividends but use payemnt dates for IRR calculation
    # If there is an irregular dividend at the end, it will need to be calculated
    # Stripped price will need to be calculated too in order to arrive at stripped yield etc

    print("Ex-div dates:")
    for item in dividend_dates_to_maturity:
        print(date_as_string(item[0]))

    print("Payment dates:")
    for item in dividend_dates_to_maturity:
        print(date_as_string(item[1]))