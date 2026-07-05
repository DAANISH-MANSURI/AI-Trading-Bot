from core.enums import Signal

from mt5.symbol_info import (
    get_stop_level,
    get_point,
    get_digits
)


def calculate_sl_tp(df, signal):

    last = df.iloc[-1]

    atr = last["ATR"]

    # ATR Based Stop Distance
    atr_distance = atr * 2

    # Broker Minimum Stop Distance
    broker_distance = get_stop_level() * get_point()

    # Final Stop Distance
    stop_distance = max(
        atr_distance,
        broker_distance
    )

    if signal == Signal.BUY:

        sl = last["close"] - stop_distance

        tp = last["close"] + (stop_distance * 2)

    elif signal == Signal.SELL:

        sl = last["close"] + stop_distance

        tp = last["close"] - (stop_distance * 2)

    else:

        return None, None

    return (
        round(sl, get_digits()),
        round(tp, get_digits())
    )