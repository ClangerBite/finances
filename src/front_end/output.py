from flask import Flask, render_template_string
from threading import Timer
from typing import List, Dict
from src.monitor.log_system import get_loggers
from src.engine.data_structures import OpenPosition, OpenAccrual
from src.front_end.open_browser import open_browser

# Get logger instances at module level
log_system, log_error, log_output = get_loggers()

class PortfolioDisplay:
    def __init__(self, open_positions: Dict[str, List[OpenPosition]], open_accruals: Dict[str, List[OpenAccrual]]):
        self.app = Flask(__name__)
        self.open_positions = open_positions
        self.open_accruals = open_accruals

        # Register routes
        self.app.add_url_rule('/', 'positions', self.show_open_positions)
        self.app.add_url_rule('/accruals', 'accruals', self.show_open_accruals)
        
    def show_open_positions(self):
        return render_template_string(
            positions_template,
            open_positions=self.open_positions,
            abs=abs
        )
        
    def show_open_accruals(self):
        return render_template_string(
            accruals_template,
            open_accruals=self.open_accruals,
            abs=abs
        )
        
    def run(self):
        Timer(1, open_browser).start()
        self.app.run(debug=False)

def display_portfolio_pages(open_positions, open_accruals):
    """Display both positions and accruals pages with navigation"""
    display = PortfolioDisplay(open_positions, open_accruals)
    display.run()



# /////////////////////////////////////////////////////////////////////////////    
# HTML TEMPLATES FOR RENDERING PAGES

positions_template = """
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
                .nav-button {
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #3498db;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    margin-bottom: 20px;
                }
                .nav-button:hover {
                    background-color: #2980b9;
                }
            </style>
        </head>
        <body>
            <a href="/accruals" class="nav-button">View Dividend Accruals</a>
            <h1>Open Positions</h1>
            <table>
                <tr>
                    <th>Ticker</th>
                    <th style="text-align: right">Quantity</th>
                    <th style="text-align: right">Price</th>
                    <th style="text-align: right">Value</th>
                    <th>Currency</th>
                </tr>
                {% for account, positions in open_positions.items() %}
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


# Add navigation to accruals template:
accruals_template = """
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
                .nav-button {
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #3498db;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    margin-bottom: 20px;
                }
                .nav-button:hover {
                    background-color: #2980b9;
                }
            </style>
        </head>
        <body>
            <a href="/" class="nav-button">View Open Positions</a>
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
                {% for account, accruals in open_accruals.items() %}
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
                            {{"{:,.6f}".format(acc.amount_per_share)}}&nbsp;
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
