import pandas as pd
from backtesting.models import TradeResult

from strategy.strategy import get_signal
from strategy.stop_loss import calculate_sl_tp

from backtesting.trade_simulator import simulate_trade
from backtesting.position_sizer import calculate_position_size
from core.enums import Signal


def execute_trade_loop(

    df,

    symbol,

    account,

    risk_percent=1

):

    """
    Execute complete trade loop.

    Parameters
    ----------
    df : pandas.DataFrame

    symbol : str

    account : AccountSimulator

    risk_percent : float

    Returns
    -------
    pandas.DataFrame
    """

    # =====================================
    # Trade Container
    # =====================================

    trades = []

    # =====================================
    # Prevent Overlapping Trades
    # =====================================

    next_available_index = 200

    # =====================================
    # Main Loop
    # =====================================

    for i in range(200, len(df) - 1):

        # Wait until previous trade closes

        if i < next_available_index:

            continue

        history = df.iloc[: i + 1].copy()

        # =====================================
        # Strategy Signal
        # =====================================

        signal = get_signal(history)

        if signal["signal"] == Signal.NO_TRADE:

            continue

        # =====================================
        # Stop Loss / Take Profit
        # =====================================

        sl, tp = calculate_sl_tp(

            history,

            signal["signal"]

        )

        if sl is None:

            continue

        # =====================================
        # Position Size
        # =====================================

        lot = calculate_position_size(

            symbol=symbol,

            balance=account.get_balance(),

            risk_percent=risk_percent,

            entry_price=history.iloc[-1]["close"],

            stop_loss=sl

        )
        # =====================================
        # Trade Simulation
        # =====================================

        trade = simulate_trade(

            df,

            i,

            signal["signal"],

            sl,

            tp

        )

        if trade is None:

            continue

        # =====================================
        # Prevent Overlapping Trades
        # =====================================

        next_available_index = trade.exit_index + 1

        # =====================================
        # Extra Trade Information
        # =====================================

        trade.sl = round(sl,2)

        trade.tp = round(tp,2)

        trade.lot_size = lot

        # =====================================
        # Account Update
        # =====================================

        trade = account.process_trade(
            trade
        )

        # =====================================
        # Save Trade
        # =====================================

        trades.append(trade)

    # =====================================
    # Convert To DataFrame
    # =====================================

    trades_df = pd.DataFrame(
        [
            trade.to_dict()

            for trade in trades
        ]
    )

    # =====================================
    # Empty Trades Handling
    # =====================================

    if trades_df.empty:

        return pd.DataFrame()

    # =====================================
    # Sort Trades
    # =====================================

    if "entry_time" in trades_df.columns:

        trades_df = trades_df.sort_values(

            by="entry_time"

        ).reset_index(drop=True)

    # =====================================
    # Return Result
    # =====================================

    return trades_df