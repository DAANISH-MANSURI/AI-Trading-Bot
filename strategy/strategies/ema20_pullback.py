"""
Professional EMA20 Pullback Strategy V2

Flow

Trend
    ↓
EMA20 Pullback
    ↓
Confirmation Candle
    ↓
WAIT_BUY / WAIT_SELL
    ↓
Trade Engine confirms breakout
"""

from core.enums import Signal, Trend

from strategy.shared.trend import get_trend

from strategy.shared.pullback import (
    bullish_pullback,
    bearish_pullback
)

from strategy.shared.confirmation import (
    bullish_confirmation,
    bearish_confirmation
)


# ==========================================================
# BUY SETUP
# ==========================================================

def bullish_setup(df):

    if len(df) < 2:
        return False

    # Trend Filter
    if get_trend(df) != Trend.BULLISH:
        return False

    # EMA20 Pullback
    if not bullish_pullback(df):
        return False

    # Confirmation Candle
    if not bullish_confirmation(df):
        return False

    return True


# ==========================================================
# SELL SETUP
# ==========================================================

def bearish_setup(df):

    if len(df) < 2:
        return False

    # Trend Filter
    if get_trend(df) != Trend.BEARISH:
        return False

    # EMA20 Pullback
    if not bearish_pullback(df):
        return False

    # Confirmation Candle
    if not bearish_confirmation(df):
        return False

    return True


# ==========================================================
# MAIN SIGNAL
# ==========================================================

def get_signal(df):

    if len(df) < 2:
        return {
            "strategy": "EMA20 Pullback",
            "trend": get_trend(df),
            "signal": Signal.NO_TRADE,
            "confidence": 0,
            "reason": "Not Enough Data",
            "setup_high": None,
            "setup_low": None,
            "entry_price": None
        }

    previous = df.iloc[-2]
    current = df.iloc[-1]

    trend = get_trend(df)

    if bullish_setup(df.iloc[:-1]) and current["high"] > previous["high"]:

        return {
            "strategy": "EMA20 Pullback",
            "trend": trend,
            "signal": Signal.BUY,
            "confidence": 90,
            "reason": "Bullish EMA20 Pullback Breakout",
            "setup_high": previous["high"],
            "setup_low": previous["low"],
            "entry_price": current["close"]
        }

    if bearish_setup(df.iloc[:-1]) and current["low"] < previous["low"]:

        return {
            "strategy": "EMA20 Pullback",
            "trend": trend,
            "signal": Signal.SELL,
            "confidence": 90,
            "reason": "Bearish EMA20 Pullback Breakout",
            "setup_high": previous["high"],
            "setup_low": previous["low"],
            "entry_price": current["close"]
        }

    return {
        "strategy": "EMA20 Pullback",
        "trend": trend,
        "signal": Signal.NO_TRADE,
        "confidence": 0,
        "reason": "No Valid Setup",
        "setup_high": None,
        "setup_low": None,
        "entry_price": None
    }