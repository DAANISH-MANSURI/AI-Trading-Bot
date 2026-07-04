from candle_patterns import (
    bullish_engulfing,
    bearish_engulfing,
    pin_bar
)

def allow_buy(df):

    last = df.iloc[-1]

    ema_ok = (
        last["EMA5"] >
        last["EMA9"] >
        last["EMA13"] >
        last["EMA21"] >
        last["EMA200"]
    )

    rsi_ok = last["RSI"] > 55

    candle_ok = bullish_engulfing(df) or pin_bar(df)

    return ema_ok and rsi_ok and candle_ok


def allow_sell(df):

    last = df.iloc[-1]

    ema_ok = (
        last["EMA5"] <
        last["EMA9"] <
        last["EMA13"] <
        last["EMA21"] <
        last["EMA200"]
    )

    rsi_ok = last["RSI"] < 45

    candle_ok = bearish_engulfing(df) or pin_bar(df)

    return ema_ok and rsi_ok and candle_ok