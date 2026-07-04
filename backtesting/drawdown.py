def calculate_drawdown(trades_df):

    if trades_df.empty:
        return {}

    balances = trades_df["balance"].tolist()

    peak_balance = balances[0]
    lowest_balance = balances[0]

    max_drawdown_amount = 0
    max_drawdown_percent = 0

    for balance in balances:

        # New Peak
        if balance > peak_balance:
            peak_balance = balance

        # Current Drawdown
        drawdown_amount = peak_balance - balance

        drawdown_percent = (
            drawdown_amount / peak_balance
        ) * 100

        # Maximum Drawdown
        if drawdown_amount > max_drawdown_amount:

            max_drawdown_amount = drawdown_amount
            max_drawdown_percent = drawdown_percent
            lowest_balance = balance

    return {

        "Peak Balance": round(peak_balance, 2),

        "Lowest Balance": round(lowest_balance, 2),

        "Maximum Drawdown ($)": round(
            max_drawdown_amount,
            2
        ),

        "Maximum Drawdown (%)": round(
            max_drawdown_percent,
            2
        )

    }