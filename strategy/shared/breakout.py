"""
Breakout Confirmation Engine
"""


# ==========================================
# BUY BREAKOUT
# ==========================================

def bullish_breakout(df):

    """
    Current candle breaks previous candle high
    """

    if len(df) < 2:
        return False

    prev = df.iloc[-2]

    last = df.iloc[-1]

    return (

        last["high"] > prev["high"]

        and

        last["close"] > prev["high"]

    )


# ==========================================
# SELL BREAKOUT
# ==========================================

def bearish_breakout(df):

    """
    Current candle breaks previous candle low
    """

    if len(df) < 2:
        return False

    prev = df.iloc[-2]

    last = df.iloc[-1]

    return (

        last["low"] < prev["low"]

        and

        last["close"] < prev["low"]

    )