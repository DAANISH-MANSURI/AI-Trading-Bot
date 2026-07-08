from backtesting.performance import calculate_performance
from backtesting.trade_analytics import analyze_trades
from backtesting.drawdown import calculate_drawdown


def calculate_statistics(
        trades_df,
        starting_balance
        ):
    """
    Calculate all backtesting statistics.

    Parameters
    ----------
    trades_df : pandas.DataFrame

    Returns
    -------
    dict
    """

    performance = calculate_performance(
        trades_df,
        starting_balance
        )

    analytics = analyze_trades(trades_df)

    drawdown = calculate_drawdown(trades_df)

    return {

        "performance": performance,

        "analytics": analytics,

        "drawdown": drawdown

    }