import os
from pathlib import Path
from datetime import datetime


def generate_html_report(
    stats,
    analytics,
    drawdown,
    trades_df
):

    # -------------------------------------
    # Paths
    # -------------------------------------

    base_path = Path(__file__).parent

    template_path = base_path / "templates" / "report_template.html"

    css_source = base_path / "assets" / "style.css"

    reports_path = Path("reports")

    reports_path.mkdir(exist_ok=True)

    css_destination = reports_path / "style.css"

    # Copy CSS
    css_destination.write_text(
        css_source.read_text(encoding="utf-8"),
        encoding="utf-8"
    )

    # Read Template
    html = template_path.read_text(
        encoding="utf-8"
    )

    # -------------------------------------
    # KPI Values
    # -------------------------------------

    final_balance = stats.get("Final Balance", 0)

    win_rate = f'{stats.get("Win Rate",0)} %'

    profit_factor = stats.get("Profit Factor",0)

    drawdown_percent = drawdown.get(
        "Maximum Drawdown (%)",
        0
    )

    # -------------------------------------
    # Tables
    # -------------------------------------

    performance_table = (
        "<table>"
    )

    for key, value in stats.items():

        performance_table += f"""
<tr>
<td>{key}</td>
<td>{value}</td>
</tr>
"""

    performance_table += "</table>"

    analytics_table = "<table>"

    for key, value in analytics.items():

        analytics_table += f"""
<tr>
<td>{key}</td>
<td>{value}</td>
</tr>
"""

    analytics_table += "</table>"

    drawdown_table = "<table>"

    for key, value in drawdown.items():

        drawdown_table += f"""
<tr>
<td>{key}</td>
<td>{value}</td>
</tr>
"""

    drawdown_table += "</table>"

    recent_trades = trades_df.tail(20).to_html(
        index=False,
        classes="trade-table"
    )

    # -------------------------------------
    # Replace Placeholders
    # -------------------------------------

    html = html.replace(
        "{{generated_time}}",
        datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    )

    html = html.replace(
        "{{win_rate}}",
        win_rate
    )

    html = html.replace(
        "{{profit_factor}}",
        str(profit_factor)
    )

    html = html.replace(
        "{{drawdown}}",
        f"{drawdown_percent}%"
    )

    html = html.replace(
        "{{performance_table}}",
        performance_table
    )

    html = html.replace(
        "{{analytics_table}}",
        analytics_table
    )

    html = html.replace(
        "{{drawdown_table}}",
        drawdown_table
    )

    html = html.replace(
        "{{recent_trades}}",
        recent_trades
    )

    # CSS path for report folder
    html = html.replace(
        "../assets/style.css",
        "style.css"
    )

    html = html.replace(
        "{{final_balance}}",
        f"${final_balance}"
    )

    # -------------------------------------
    # Save Report
    # -------------------------------------

    report_file = reports_path / "backtest_report.html"

    report_file.write_text(
        html,
        encoding="utf-8"
    )

    print()
    print("✅ HTML Report Generated")
    print(report_file)