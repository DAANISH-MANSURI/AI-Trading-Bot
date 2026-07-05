def calculate_performance(
        trades_df,
        starting_balance
):

    if trades_df.empty:

        return {

            "Total Trades": 0

        }

    # ==========================================
    # Basic Stats
    # ==========================================

    total_trades = len(trades_df)

    wins = len(
        trades_df[
            trades_df["result"] == "WIN"
        ]
    )

    losses = len(
        trades_df[
            trades_df["result"] == "LOSS"
        ]
    )

    win_rate = (
        wins / total_trades
    ) * 100

    # ==========================================
    # Balance
    # ==========================================


    final_balance = trades_df.iloc[-1]["balance"]

    net_profit = final_balance - starting_balance

    return_percent = (
        net_profit / starting_balance
    ) * 100

    # ==========================================
    # Profit Statistics
    # ==========================================

    gross_profit = trades_df[
        trades_df["profit"] > 0
    ]["profit"].sum()

    gross_loss = abs(
        trades_df[
            trades_df["profit"] < 0
        ]["profit"].sum()
    )

    if gross_loss == 0:

        profit_factor = float("inf")

    else:

        profit_factor = gross_profit / gross_loss

    average_profit = trades_df[
        "profit"
    ].mean()

    largest_win = trades_df[
        "profit"
    ].max()

    largest_loss = trades_df[
        "profit"
    ].min()

    average_duration = trades_df[
        "trade_duration"
    ].mean()

    # ==========================================
    # Report
    # ==========================================

    return {

        "Starting Balance": round(starting_balance, 2),

        "Final Balance": round(final_balance, 2),

        "Net Profit": round(net_profit, 2),

        "Return %": round(return_percent, 2),

        "Total Trades": total_trades,

        "Wins": wins,

        "Losses": losses,

        "Win Rate": round(win_rate, 2),

        "Gross Profit": round(gross_profit, 2),

        "Gross Loss": round(gross_loss, 2),

        "Profit Factor": round(profit_factor, 2),

        "Average Profit": round(average_profit, 2),

        "Largest Win": round(largest_win, 2),

        "Largest Loss": round(largest_loss, 2),

        "Average Duration": round(average_duration, 2)

    }