"""
EMA Cross Quality Filter
"""

EMA_DISTANCE_ATR = 0.10


def bullish_cross_valid(df):
    """
    Bullish cross should have enough EMA separation.
    """

    last = df.iloc[-1]

    ema9 = last["EMA9"]
    ema20 = last["EMA20"]

    atr = last["ATR"]

    distance = abs(ema9 - ema20)

    return distance >= atr * EMA_DISTANCE_ATR


def bearish_cross_valid(df):
    """
    Bearish cross should have enough EMA separation.
    """

    last = df.iloc[-1]

    ema9 = last["EMA9"]
    ema20 = last["EMA20"]

    atr = last["ATR"]

    distance = abs(ema9 - ema20)

    return distance >= atr * EMA_DISTANCE_ATR