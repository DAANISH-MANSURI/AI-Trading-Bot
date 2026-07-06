"""
Trend Detection Engine

EMA Pullback Strategy
"""

from core.enums import Trend


# ==========================================
# EMA Slope
# ==========================================

def ema_rising(df, ema="EMA20", bars=3):

    if len(df) < bars + 1:
        return False

    recent = df[ema].tail(bars + 1).values

    for i in range(1, len(recent)):

        if recent[i] <= recent[i - 1]:
            return False

    return True


def ema_falling(df, ema="EMA20", bars=3):

    if len(df) < bars + 1:
        return False

    recent = df[ema].tail(bars + 1).values

    for i in range(1, len(recent)):

        if recent[i] >= recent[i - 1]:
            return False

    return True


# ==========================================
# Bullish Trend
# ==========================================

def is_bullish(df):

    last = df.iloc[-1]

    return (

        last["EMA9"] > last["EMA20"]

        and

        last["close"] > last["EMA9"]

        and

        last["close"] > last["EMA20"]

        and

        ema_rising(df)

    )


# ==========================================
# Bearish Trend
# ==========================================

def is_bearish(df):

    last = df.iloc[-1]

    return (

        last["EMA9"] < last["EMA20"]

        and

        last["close"] < last["EMA9"]

        and

        last["close"] < last["EMA20"]

        and

        ema_falling(df)

    )


# ==========================================
# Current Trend
# ==========================================

def get_trend(df):

    if is_bullish(df):
        return Trend.BULLISH

    if is_bearish(df):
        return Trend.BEARISH

    return Trend.SIDEWAYS