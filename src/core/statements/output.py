from flask import Flask, render_template_string
from threading import Timer
from typing import List, Dict
from monitor.log_system import get_loggers
from core.statements.data_structures import OpenPosition, OpenAccrual
from core.statements.open_browser import open_browser

# Get logger instances at module level
log_system, log_error, log_output = get_loggers()



def display_open_positions_page(open_pos: Dict[str, List[OpenPosition]]) -> None:
    """Output open positions for each account to HTML table"""
    
    app = Flask(__name__)
    
    html_template = """
    <html>
        <head>
            <title>Portfolio Positions</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    background-color: #f5f5f5;
                }
                h2 {
                    color: #2c3e50;
                    border-bottom: 2px solid #3498db;
                    padding-bottom: 10px;
                    margin-top: 30px;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }
                th {
                    background-color: #3498db;
                    color: white;
                    padding: 12px;
                    text-align: left;
                }
                td {
                    padding: 8px;
                    border-bottom: 1px solid #ddd;
                }
                tr:hover {
                    background-color: #f0f7fa;
                }
                .currency-usd { color: #27ae60; }
                .currency-gbp { color: #8e44ad; }
                .value-cell {
                    text-align: right;
                    font-family: monospace;
                    white-space: pre;
                    padding-right: 10px;
                }            
                .negative { color: #e74c3c; }
                .account-header {
                    background-color: #f8f9fa;
                    font-weight: bold;
                    text-align: left;
                    padding: 10px;
                    border-top: 2px solid #dee2e6;
                }
            </style>
        </head>
        <body>
            <h1>Open Positions</h1>
            <table>
                <tr>
                    <th>Ticker</th>
                    <th style="text-align: right">Quantity</th>
                    <th style="text-align: right">Price</th>
                    <th style="text-align: right">Value</th>
                    <th>Currency</th>
                </tr>
                {% for account, positions in open_pos.items() %}
                    <tr>
                        <td colspan="5" class="account-header">{{account}}</td>
                    </tr>
                    {% for pos in positions %}
                    <tr>
                        <td>{{pos.ticker}}</td>
                        <td class="value-cell">
                            {%- if pos.quantity < 0 -%}
                                ({{"{:,.0f}".format(abs(pos.quantity))}})
                            {%- else -%}
                                {{"{:,.0f}".format(pos.quantity)}}&nbsp;
                            {%- endif -%}
                        </td>
                        <td class="value-cell">
                            {%- if pos.price < 0 -%}
                                ({{"{:,.3f}".format(abs(pos.price))}})
                            {%- else -%}
                                {{"{:,.3f}".format(pos.price)}}&nbsp;
                            {%- endif -%}
                        </td>
                        <td class="value-cell">
                            {%- if pos.value < 0 -%}
                                ({{"{:,.2f}".format(abs(pos.value))}})
                            {%- else -%}
                                {{"{:,.2f}".format(pos.value)}}&nbsp;
                            {%- endif -%}
                        </td>
                        <td class="currency-{{pos.currency.lower()}}">{{pos.currency}}</td>
                    </tr>
                    {% endfor %}
                {% endfor %}
            </table>
        </body>
    </html>
    """
    
    # Create template context with abs function
    template_context = {
        'open_pos': open_pos,
        'abs': abs  # Make abs() available to template
    }
    
    @app.route('/')
    def show_positions():
        return render_template_string(
            html_template,  # First argument is the template string
            open_pos=open_pos,  # Then pass context variables as kwargs
            abs=abs  # Make abs() available to template
        )
    
    # Open browser after a short delay to ensure server is running
    Timer(1, open_browser).start()
    
    # Run the Flask app
    app.run(debug=False)
    
        

def display_open_accruals_page(open_acc: Dict[str, List[OpenAccrual]]) -> None:
    """Output open accruals to browser with HTML formatting"""
    app = Flask(__name__)
    
    html_template = """
    <html>
        <head>
            <title>Dividend Accruals</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    background-color: #f5f5f5;
                }
                h2 {
                    color: #2c3e50;
                    border-bottom: 2px solid #3498db;
                    padding-bottom: 10px;
                    margin-top: 30px;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }
                th {
                    background-color: #3498db;
                    color: white;
                    padding: 12px;
                    text-align: left;
                }
                td {
                    padding: 8px;
                    border-bottom: 1px solid #ddd;
                }
                tr:hover {
                    background-color: #f0f7fa;
                }
                .currency-usd { color: #27ae60; }
                .currency-gbp { color: #8e44ad; }
                .value-cell {
                    text-align: right;
                    font-family: monospace;
                    white-space: pre;
                    padding-right: 10px;
                }            
                .negative { color: #e74c3c; }
                .account-header {
                    background-color: #f8f9fa;
                    font-weight: bold;
                    text-align: left;
                    padding: 10px;
                    border-top: 2px solid #dee2e6;
                }
            </style>
        </head>
        <body>
            <table>
                <tr>
                    <th>Ticker</th>
                    <th style="text-align: right">Quantity</th>
                    <th style="text-align: right">Amount/Share</th>
                    <th style="text-align: right">Gross Amount</th>
                    <th style="text-align: right">Tax</th>
                    <th style="text-align: right">Net Amount</th>
                    <th>Currency</th>
                    <th>Ex-Date</th>
                    <th>Pay Date</th>
                </tr>
                {% for account, accruals in open_acc.items() %}
                    <tr>
                        <td colspan="9" class="account-header">{{account}}</td>
                    </tr>
                    {% for acc in accruals %}
                    <tr>
                        <td>{{acc.ticker}}</td>
                        <td class="value-cell">
                            {%- if acc.quantity < 0 -%}
                                ({{"{:,.0f}".format(abs(acc.quantity))}})
                            {%- else -%}
                                {{"{:,.0f}".format(acc.quantity)}}&nbsp;
                            {%- endif -%}
                        </td>
                        <td class="value-cell">
                            {{"{:,.4f}".format(acc.amount_per_share)}}&nbsp;
                        </td>
                        <td class="value-cell">
                            {%- if acc.gross_amount < 0 -%}
                                ({{"{:,.2f}".format(abs(acc.gross_amount))}})
                            {%- else -%}
                                {{"{:,.2f}".format(acc.gross_amount)}}&nbsp;
                            {%- endif -%}
                        </td>
                        <td class="value-cell">
                            {%- if acc.withholding_tax < 0 -%}
                                ({{"{:,.2f}".format(abs(acc.withholding_tax))}})
                            {%- else -%}
                                {{"{:,.2f}".format(acc.withholding_tax)}}&nbsp;
                            {%- endif -%}
                        </td>
                        <td class="value-cell">
                            {%- if acc.net_amount < 0 -%}
                                ({{"{:,.2f}".format(abs(acc.net_amount))}})
                            {%- else -%}
                                {{"{:,.2f}".format(acc.net_amount)}}&nbsp;
                            {%- endif -%}
                        </td>
                        <td>{{acc.currency}}</td>
                        <td>{{acc.ex_date.strftime('%Y-%m-%d')}}</td>
                        <td>{{acc.pay_date.strftime('%Y-%m-%d')}}</td>
                    </tr>
                    {% endfor %}
                {% endfor %}
            </table>
        </body>
    </html>
    """
    
      # Create template context with abs function
    template_context = {
        'open_acc': open_acc,
        'abs': abs  # Make abs() available to template
    }
    
    @app.route('/')
    def show_positions():
        return render_template_string(
            html_template,  # First argument is the template string
            open_acc=open_acc,  # Then pass context variables as kwargs
            abs=abs  # Make abs() available to template
        )
        
      # Open browser after a short delay to ensure server is running
    Timer(1, open_browser).start()
    
    app.run(debug=False)

