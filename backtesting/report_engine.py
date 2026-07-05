import os

from backtesting.equity_curve import generate_equity_curve
from backtesting.report_generator import generate_html_report


def save_reports(

    trades_df,

    performance,

    analytics,

    drawdown,

    reports_dir="reports"

):
    """
    Save all backtesting reports.

    Parameters
    ----------
    trades_df : pandas.DataFrame

    performance : dict

    analytics : dict

    drawdown : dict

    reports_dir : str
    """

    # ==========================================
    # Create Reports Folder
    # ==========================================

    os.makedirs(

        reports_dir,

        exist_ok=True

    )

    # ==========================================
    # CSV Report
    # ==========================================

    csv_path = os.path.join(

        reports_dir,

        "backtest_results.csv"

    )

    trades_df.to_csv(

        csv_path,

        index=False

    )

    # ==========================================
    # Equity Curve
    # ==========================================

    generate_equity_curve(

        trades_df

    )

    # ==========================================
    # HTML Report
    # ==========================================

    html_path = generate_html_report(

        performance,

        analytics,

        drawdown,

        trades_df

    )

    # ==========================================
    # Return File Paths
    # ==========================================

    return {

        "csv": csv_path,

        "equity_curve": os.path.join(

            reports_dir,

            "equity_curve.png"

        ),

        "html": html_path

    }