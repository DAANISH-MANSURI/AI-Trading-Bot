import pandas as pd


def analyze_trades(trades_df):

    if trades_df.empty:

        return {}

    report = {}

    # ==========================================
    # BUY Trades
    # ==========================================

    buy = trades_df[trades_df["signal"] == "BUY"]

    buy_wins = len(buy[buy["result"] == "WIN"])
    buy_losses = len(buy[buy["result"] == "LOSS"])

    buy_win_rate = (
        buy_wins / len(buy) * 100
        if len(buy) > 0 else 0
    )

    report["BUY Trades"] = len(buy)
    report["BUY Wins"] = buy_wins
    report["BUY Losses"] = buy_losses
    report["BUY Win Rate"] = round(buy_win_rate, 2)

    # ==========================================
    # SELL Trades
    # ==========================================

    sell = trades_df[trades_df["signal"] == "SELL"]

    sell_wins = len(sell[sell["result"] == "WIN"])
    sell_losses = len(sell[sell["result"] == "LOSS"])

    sell_win_rate = (
        sell_wins / len(sell) * 100
        if len(sell) > 0 else 0
    )

    report["SELL Trades"] = len(sell)
    report["SELL Wins"] = sell_wins
    report["SELL Losses"] = sell_losses
    report["SELL Win Rate"] = round(sell_win_rate, 2)

    # ==========================================
    # Average Trade Duration
    # ==========================================

    report["Average BUY Duration"] = round(
        buy["trade_duration"].mean(), 2
    ) if len(buy) else 0

    report["Average SELL Duration"] = round(
        sell["trade_duration"].mean(), 2
    ) if len(sell) else 0

    # ==========================================
    # Average Profit
    # ==========================================

    report["Average BUY Profit"] = round(
        buy["profit"].mean(), 2
    ) if len(buy) else 0

    report["Average SELL Profit"] = round(
        sell["profit"].mean(), 2
    ) if len(sell) else 0

    # ==========================================
    # Total Profit
    # ==========================================

    report["BUY Net Profit"] = round(
        buy["profit"].sum(), 2
    )

    report["SELL Net Profit"] = round(
        sell["profit"].sum(), 2
    )

    return report