from backtesting.models import TradeResult
from core.enums import Signal, TradeStatus, ExitReason


def simulate_trade(
    df,
    entry_index,
    signal,
    entry_price,
    sl,
    tp
):
    """
    Trade Simulator V2

    Entry comes from Trade Engine.
    """

    entry_candle = df.iloc[entry_index]

    entry_time = entry_candle["time"]

    # =====================================
    # Risk & Reward
    # =====================================

    risk_points = abs(entry_price - sl)
    reward_points = abs(tp - entry_price)

    if risk_points <= 0:
        return None

    rr = round(reward_points / risk_points, 2)

    # =====================================
    # Candle Loop
    # =====================================

    for i in range(entry_index + 1, len(df)):

        candle = df.iloc[i]

        exit_time = candle["time"]

        high = candle["high"]
        low = candle["low"]

        duration = i - entry_index

        # =====================================
        # BUY
        # =====================================

        if signal == Signal.BUY:

            # Stop Loss

            if low <= sl:

                return TradeResult(

                    signal=signal.value,

                    result=TradeStatus.LOSS.value,

                    entry_time=entry_time,

                    exit_time=exit_time,

                    entry_price=round(entry_price, 2),

                    exit_price=round(sl, 2),

                    sl=round(sl, 2),

                    tp=round(tp, 2),

                    lot_size=0,

                    profit=0,

                    balance=0,

                    risk_amount=0,

                    rr=rr,

                    trade_duration=duration,

                    exit_reason=ExitReason.SL.value,

                    exit_index=i

                )

            # Take Profit

            if high >= tp:

                return TradeResult(

                    signal=signal.value,

                    result=TradeStatus.WIN.value,

                    entry_time=entry_time,

                    exit_time=exit_time,

                    entry_price=round(entry_price, 2),

                    exit_price=round(tp, 2),

                    sl=round(sl, 2),

                    tp=round(tp, 2),

                    lot_size=0,

                    profit=0,

                    balance=0,

                    risk_amount=0,

                    rr=rr,

                    trade_duration=duration,

                    exit_reason=ExitReason.TP.value,

                    exit_index=i

                )

        # =====================================
        # SELL
        # =====================================

        elif signal == Signal.SELL:

            # Stop Loss

            if high >= sl:

                return TradeResult(

                    signal=signal.value,

                    result=TradeStatus.LOSS.value,

                    entry_time=entry_time,

                    exit_time=exit_time,

                    entry_price=round(entry_price, 2),

                    exit_price=round(sl, 2),

                    sl=round(sl, 2),

                    tp=round(tp, 2),

                    lot_size=0,

                    profit=0,

                    balance=0,

                    risk_amount=0,

                    rr=rr,

                    trade_duration=duration,

                    exit_reason=ExitReason.SL.value,

                    exit_index=i

                )

            # Take Profit

            if low <= tp:

                return TradeResult(

                    signal=signal.value,

                    result=TradeStatus.WIN.value,

                    entry_time=entry_time,

                    exit_time=exit_time,

                    entry_price=round(entry_price, 2),

                    exit_price=round(tp, 2),

                    sl=round(sl, 2),

                    tp=round(tp, 2),

                    lot_size=0,

                    profit=0,

                    balance=0,

                    risk_amount=0,

                    rr=rr,

                    trade_duration=duration,

                    exit_reason=ExitReason.TP.value,

                    exit_index=i

                )

    return None