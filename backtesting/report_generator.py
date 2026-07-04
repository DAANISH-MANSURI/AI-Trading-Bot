import os


def generate_html_report(
    stats,
    analytics,
    drawdown,
    trades_df
):

    os.makedirs("reports", exist_ok=True)

    html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<title>AI Trading Bot Report</title>

<style>

body{{
font-family:Arial;
background:#f5f5f5;
margin:40px;
}}

h1{{
color:#222;
}}

table{{
border-collapse:collapse;
width:100%;
margin-bottom:30px;
}}

th,td{{
border:1px solid #ccc;
padding:8px;
text-align:left;
}}

th{{
background:#222;
color:white;
}}

.card{{
background:white;
padding:20px;
margin-bottom:20px;
border-radius:10px;
box-shadow:0 0 10px rgba(0,0,0,.15);
}}

img{{
width:100%;
max-width:900px;
}}

</style>

</head>

<body>

<h1>AI Trading Bot Backtest Report</h1>

<div class="card">

<h2>Performance Report</h2>

<table>
"""

    for k, v in stats.items():
        html += f"<tr><td>{k}</td><td>{v}</td></tr>"

    html += """
</table>

</div>

<div class="card">

<h2>Trade Analytics</h2>

<table>
"""

    for k, v in analytics.items():
        html += f"<tr><td>{k}</td><td>{v}</td></tr>"

    html += """
</table>

</div>

<div class="card">

<h2>Drawdown Report</h2>

<table>
"""

    for k, v in drawdown.items():
        html += f"<tr><td>{k}</td><td>{v}</td></tr>"

    html += """
</table>

</div>

<div class="card">

<h2>Equity Curve</h2>

<img src="equity_curve.png">

</div>

<div class="card">

<h2>Last 20 Trades</h2>
"""

    html += trades_df.tail(20).to_html(index=False)

    html += """

</div>

</body>

</html>

"""

    with open(
        "reports/backtest_report.html",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html)