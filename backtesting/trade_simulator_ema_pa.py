"""
Trade Simulator for EMA 9/20 + Price Action Strategy.

Simulates trades with exit conditions:
- Stop Loss (SL) hit (priority)
- EMA cross-back exit (EMA9 crosses EMA20 against the trade direction)
No fixed Take Profit (TP) is used for exit logic; a notional TP based on
2.0 risk-reward is included in the TradeResult for compatibility.
"""

from backtesting.models import TradeResult
from core.enums import Signal, TradeStatus, ExitReason
from strategy.strategies.ema_price_action import detect_crossover


def simulate_trade_ema_pa(df, entry_index, signal, entry_price, sl):
    """
    Simulate a trade for the EMA 9/20 + Price Action strategy.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with OHLCV data and indicators (EMA9, EMA20, etc.).
    entry_index : int
        Index of the entry candle in df.
    signal : Signal
        Signal.BUY or Signal.SELL.
    entry_price : float
        Price at which the trade was entered.
    sl : float
        Stop loss price.

    Returns
    -------
    TradeResult or None
        TradeResult if the trade exited (SL hit or EMA cross-back), None if
        the trade remains open (to be handled by the trade engine's
        next_available_index logic).
    """
    # Basic validation
    if df is None or len(df) == 0:
        return None
    if entry_index < 0 or entry_index >= len(df):
        return None
    if sl is None:
        return None

    # Calculate risk and validate
    risk = abs(entry_price - sl)
    if risk <= 0:
        return None

    # Notional TP for TradeResult compatibility (not used for exit logic)
    if signal == Signal.BUY:
        notional_tp = entry_price + 2.0 * risk
    else:  # Signal.SELL
        notional_tp = entry_price - 2.0 * risk

    # Loop from the next candle after entry to the end
    for i in range(entry_index + 1, len(df)):
        candle = df.iloc[i]
        exit_price = None
        exit_reason = None
        win = None

        # 1. Check SL hit first (priority)
        if signal == Signal.BUY:
            if candle["low"] <= sl:
                exit_price = sl
                exit_reason = ExitReason.SL
                win = False  # SL hit is a loss for BUY
        else:  # Signal.SELL
            if candle["high"] >= sl:
                exit_price = sl
                exit_reason = ExitReason.SL
                win = False  # SL hit is a loss for SELL

        if exit_price is not None:
            # SL hit, break out
            break

        # 2. Check EMA cross-back exit (only if we have at least two candles for crossover)
        if i >= entry_index + 1:  # need previous and current candle
            df_sub = df.iloc[i-1:i+1]  # two candles: [i-1, i]
            crossover = detect_crossover(df_sub)
            if signal == Signal.BUY:
                if crossover == "BEARISH_CROSS":
                    exit_price = candle["close"]
                    exit_reason = ExitReason.EMA_EXIT
                    win = exit_price > entry_price
            else:  # Signal.SELL
                if crossover == "BULLISH_CROSS":
                    exit_price = candle["close"]
                    exit_reason = ExitReason.EMA_EXIT
                    win = exit_price < entry_price

        if exit_price is not None:
            # EMA cross-back exit, break out
            break

    # If we never set an exit price, the trade is still open
    if exit_price is None:
        return None

    # Calculate realized risk-reward (based on actual exit)
    reward = abs(exit_price - entry_price)
    # risk is already defined as abs(entry_price - sl) and we know it's > 0
    rr = reward / risk if risk != 0 else None

    # Build and return TradeResult
    # Note: We round prices to 2 decimal places to match the existing simulator's behavior
    # The trade engine will later round to the symbol's digit precision if needed
    return TradeResult(
        signal=signal.value,
        result=TradeStatus.WIN.value if win else TradeStatus.LOSS.value,
        entry_time=df.iloc[entry_index]["time"],
        exit_time=candle["time"],
        entry_price=round(entry_price, 2),
        exit_price=round(exit_price, 2),
        sl=round(sl, 2),
        tp=round(notional_tp, 2),  # notional TP for informational purposes only
        lot_size=0,
        profit=0,
        balance=0,
        risk_amount=0,
        rr=rr,
        trade_duration=i - entry_index,
        exit_reason=exit_reason.value,
        exit_index=i
    )