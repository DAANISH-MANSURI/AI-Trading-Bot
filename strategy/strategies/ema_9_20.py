"""
EMA 9 / EMA 20 Pullback Strategy
"""

from core.enums import Signal

from strategy.shared.trend import get_trend

from strategy.shared.pullback import (
    bullish_pullback,
    bearish_pullback
)

from strategy.shared.confirmation import (
    bullish_confirmation,
    bearish_confirmation
)


# ==========================================
# Fresh Cross
# ==========================================

def bullish_cross(df):

    """
    EMA9 crosses above EMA20
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
    EMA9 crosses below EMA20
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


# ==========================================
# BUY SETUP
# ==========================================

def bullish_setup(df):

    if not bullish_pullback(df):

        return False

    if not bullish_confirmation(df):

        return False

    return True


# ==========================================
# SELL SETUP
# ==========================================

def bearish_setup(df):

    if not bearish_pullback(df):

        return False

    if not bearish_confirmation(df):

        return False

    return True


# ==========================================
# MAIN SIGNAL
# ==========================================

def get_signal(df):

    trend = get_trend(df)

    # -----------------------------
    # BUY
    # -----------------------------

    if trend.name == "BULLISH":

        if bullish_setup(df):

            return {

                "strategy": "EMA 9/20",

                "trend": trend,

                "signal": Signal.BUY,

                "confidence": 80,

                "reason": "Bullish EMA Pullback"

            }

        return {

            "strategy": "EMA 9/20",

            "trend": trend,

            "signal": Signal.NO_TRADE,

            "confidence": 60,

            "reason": "Waiting For Pullback"

        }

    # -----------------------------
    # SELL
    # -----------------------------

    if trend.name == "BEARISH":

        if bearish_setup(df):

            return {

                "strategy": "EMA 9/20",

                "trend": trend,

                "signal": Signal.SELL,

                "confidence": 80,

                "reason": "Bearish EMA Pullback"

            }

        return {

            "strategy": "EMA 9/20",

            "trend": trend,

            "signal": Signal.NO_TRADE,

            "confidence": 60,

            "reason": "Waiting For Pullback"

        }

    # -----------------------------
    # SIDEWAYS
    # -----------------------------

    return {

        "strategy": "EMA 9/20",

        "trend": trend,

        "signal": Signal.NO_TRADE,

        "confidence": 20,

        "reason": "Sideways Market"

    }