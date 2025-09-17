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
                border-collapse: collapse;
                width: 100%;
                margin-bottom: 30px;
                background-color: white;
                box-shadow: 0 1px 3px rgba(0,0,0,0.2);
                font-variant-numeric: tabular-nums;  /* Ensures all numbers have same width */
            }
            th {
                background-color: #3498db;
                color: white;
                padding: 12px;
                text-align: left;
                font-weight: bold;
            }
            td {
                padding: 10px;
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
        </style>
    </head>
    <body>
        {% for account, positions in open_pos.items() %}
            <h2>{{account}}</h2>
            <table>
                <tr>
                    <th>Ticker</th>
                    <th style="text-align: right">Quantity</th>
                    <th style="text-align: right">Price</th>
                    <th style="text-align: right">Value</th>
                    <th>Currency</th>
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
            </table>
        {% endfor %}
    </body>
</html>
"""