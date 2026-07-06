"""
Professional EMA20 Pullback Engine
"""

from strategy.shared.helpers import within_tolerance


BODY_PERCENT = 0.50


def strong_bullish_body(last):

    body = abs(last["close"] - last["open"])

    candle = last["high"] - last["low"]

    if candle == 0:
        return False

    return (

        last["close"] > last["open"]

        and

        body >= candle * BODY_PERCENT

    )


def strong_bearish_body(last):

    body = abs(last["close"] - last["open"])

    candle = last["high"] - last["low"]

    if candle == 0:
        return False

    return (

        last["close"] < last["open"]

        and

        body >= candle * BODY_PERCENT

    )


def bullish_pullback(
    df,
    atr_multiplier=0.25
):

    if len(df) < 2:
        return False

    last = df.iloc[-1]
    prev = df.iloc[-2]

    ema20 = last["EMA20"]

    atr = last["ATR"]

    tolerance = atr * atr_multiplier

    touch = within_tolerance(

        last["low"],

        ema20,

        tolerance

    )

    if not touch:
        return False

    if prev["close"] <= prev["EMA20"]:
        return False

    if last["close"] <= ema20:
        return False

    if not strong_bullish_body(last):
        return False

    return True


def bearish_pullback(
    df,
    atr_multiplier=0.25
):

    if len(df) < 2:
        return False

    last = df.iloc[-1]
    prev = df.iloc[-2]

    ema20 = last["EMA20"]

    atr = last["ATR"]

    tolerance = atr * atr_multiplier

    touch = within_tolerance(

        last["high"],

        ema20,

        tolerance

    )

    if not touch:
        return False

    if prev["close"] >= prev["EMA20"]:
        return False

    if last["close"] >= ema20:
        return False

    if not strong_bearish_body(last):
        return False

    return True