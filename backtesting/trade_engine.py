from mt5.symbol_info import get_digits
from config.trading import RISK_PERCENT

import pandas as pd
from backtesting.models import TradeResult

from strategy.strategies.ema_price_action import get_signal, reset_state
from backtesting.position_sizer import calculate_position_size
from core.enums import Signal
from backtesting.trade_simulator_ema_pa import simulate_trade_ema_pa

WINDOW_SIZE = 300

def execute_trade_loop(

    df,

    symbol,

    account,

    risk_percent=RISK_PERCENT,

    htf_df=None

):

    """

    Execute complete trade loop.

    Parameters
    ----------
    df : pandas.DataFrame

    symbol : str

    account : AccountSimulator

    risk_percent : float

    htf_df : pandas.DataFrame, optional
        Higher timeframe data for bias calculation

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

        start = max(0, i - WINDOW_SIZE + 1)
        history = df.iloc[start : i + 1].copy()
        # Set symbol attribute for strategies that need it
        history.attrs["symbol"] = symbol
        # Set HTF data and current time for bias calculation
        if htf_df is not None:
            history.attrs["htf_df"] = htf_df
            history.attrs["current_time"] = history.iloc[-1]["time"]

        signal = get_signal(history)

        if signal["signal"] in (
            Signal.WAIT_BUY,
            Signal.WAIT_SELL,
            Signal.NO_TRADE
        ):

            continue

        # =====================================
        # Stop Loss / Take Profit
        # =====================================

        # Extract SL from signal (already calculated by strategy)
        if signal["signal"] == Signal.BUY:
            sl = signal["setup_low"]
        else:  # Signal.SELL
            sl = signal["setup_high"]
        if sl is None:
            continue
        entry_price = history.iloc[-1]["close"]
        if abs(sl - entry_price) < 1e-9:  # zero-risk guard
            continue

        # =====================================
        # Position Size
        # =====================================


        lot = calculate_position_size(

            symbol=symbol,

            balance=account.get_balance(),

            risk_percent=risk_percent,

            entry_price=entry_price,

            stop_loss=sl

        )
        # =====================================
        # Trade Simulation
        # =====================================

        trade = simulate_trade_ema_pa(
            df,
            i,
            signal["signal"],
            entry_price,
            sl
        )

        if trade is None:
            reset_state(symbol) #reset symbol state
            continue

        # =====================================
        # Prevent Overlapping Trades
        # =====================================

        next_available_index = trade.exit_index + 1

        # =====================================
        # Extra Trade Information
        # =====================================

        digits = get_digits()

        trade.sl = round(sl, digits)

        trade.tp = None  # strategy has no fixed TP, exits on EMA cross-back / trailing SL

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
        # Reset strategy state for this symbol since the trade has been processed
        reset_state(symbol)

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