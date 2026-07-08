"""
EMA 9 / EMA 20 Crossover Strategy

BUY
EMA9 crosses ABOVE EMA20

SELL
EMA9 crosses BELOW EMA20
"""
from strategy.shared.cross_filter import (
    bullish_cross_valid,
    bearish_cross_valid
)
from core.enums import Signal, Trend

from strategy.shared.trend import get_trend


# ==========================================================
# CROSS DETECTION
# ==========================================================

def bullish_cross(df):
    """
    EMA9 crosses ABOVE EMA20
    """

    if len(df) < 2:
        return False

    prev = df.iloc[-2]
    last = df.iloc[-1]

    return (

        prev["EMA9"] <= prev["EMA20"]

        and

        last["EMA9"] > last["EMA20"]

    )


def bearish_cross(df):
    """
    EMA9 crosses BELOW EMA20
    """

    if len(df) < 2:
        return False

    prev = df.iloc[-2]
    last = df.iloc[-1]

    return (

        prev["EMA9"] >= prev["EMA20"]

        and

        last["EMA9"] < last["EMA20"]

    )


# ==========================================================
# BUY SETUP
# ==========================================================

def bullish_setup(df):

    if not bullish_cross(df):
        return False
    
    if not bullish_cross_valid(df):
        return False

    last = df.iloc[-1]

    # Bullish confirmation candle
    if last["close"] <= last["open"]:
        return False

    return True


# ==========================================================
# SELL SETUP
# ==========================================================

def bearish_setup(df):

    if not bearish_cross(df):
        return False
    
    if not bearish_cross_valid(df):
        return False

    last = df.iloc[-1]

    # Bearish confirmation candle
    if last["close"] >= last["open"]:
        return False

    return True


# ==========================================================
# MAIN SIGNAL
# ==========================================================

def get_signal(df):

    trend = get_trend(df)

    # BUY

    if bullish_setup(df):

        return {

            "strategy": "EMA 9/20 Crossover",

            "trend": Trend.BULLISH,

            "signal": Signal.BUY,

            "confidence": 90,

            "reason": "Bullish EMA Cross"

        }

    # SELL

    if bearish_setup(df):

        return {

            "strategy": "EMA 9/20 Crossover",

            "trend": Trend.BEARISH,

            "signal": Signal.SELL,

            "confidence": 90,

            "reason": "Bearish EMA Cross"

        }

    # NO TRADE

    return {

        "strategy": "EMA 9/20 Crossover",

        "trend": trend,

        "signal": Signal.NO_TRADE,

        "confidence": 0,

        "reason": "No EMA Cross"

    }