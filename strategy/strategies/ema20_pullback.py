"""
Professional EMA20 Pullback Strategy V2

Flow

Trend
    ↓
EMA20 Pullback
    ↓
Confirmation Candle
    ↓
Breakout
    ↓
BUY / SELL
"""

from core.enums import Signal, Trend

from config.strategy import DEBUG_STRATEGY

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

    if get_trend(df) != Trend.BULLISH:
        return False

    if not bullish_pullback(df):
        return False

    if not bullish_confirmation(df):
        return False

    return True


# ==========================================================
# SELL SETUP
# ==========================================================

def bearish_setup(df):

    if len(df) < 2:
        return False

    if get_trend(df) != Trend.BEARISH:
        return False

    if not bearish_pullback(df):
        return False

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

    setup_df = df.iloc[:-1]

    # ======================================
    # DEBUG VALUES
    # ======================================

    bull_pullback = bullish_pullback(setup_df)
    bear_pullback = bearish_pullback(setup_df)

    bull_confirmation = bullish_confirmation(setup_df)
    bear_confirmation = bearish_confirmation(setup_df)

    bull_setup = bullish_setup(setup_df)
    bear_setup = bearish_setup(setup_df)

    buy_breakout = current["high"] > previous["high"]
    sell_breakout = current["low"] < previous["low"]

    if DEBUG_STRATEGY:

        print()
        print("=" * 65)
        print("EMA20 PULLBACK DEBUG")
        print("=" * 65)

        print(f"Trend                  : {trend}")

        print()

        print(f"Bullish Pullback       : {bull_pullback}")
        print(f"Bearish Pullback       : {bear_pullback}")

        print()

        print(f"Bullish Confirmation   : {bull_confirmation}")
        print(f"Bearish Confirmation   : {bear_confirmation}")

        print()

        print(f"Bullish Setup          : {bull_setup}")
        print(f"Bearish Setup          : {bear_setup}")

        print()

        print(f"Previous High          : {previous['high']:.5f}")
        print(f"Current High           : {current['high']:.5f}")
        print(f"BUY Breakout           : {buy_breakout}")

        print()

        print(f"Previous Low           : {previous['low']:.5f}")
        print(f"Current Low            : {current['low']:.5f}")
        print(f"SELL Breakout          : {sell_breakout}")

        print("=" * 65)

    # ======================================
    # DEBUG FAILURE REASON
    # ======================================

    if DEBUG_STRATEGY:

        print()
        print("CHECKLIST")

        if trend != Trend.BULLISH and trend != Trend.BEARISH:
            print("❌ Trend Filter Failed")

        if not bull_pullback and not bear_pullback:
            print("❌ Pullback Failed")

        if not bull_confirmation and not bear_confirmation:
            print("❌ Confirmation Failed")

        if bull_setup and not buy_breakout:
            print("❌ BUY Breakout Pending")

        if bear_setup and not sell_breakout:
            print("❌ SELL Breakout Pending")

        if (
            trend in (Trend.BULLISH, Trend.BEARISH)
            and (bull_pullback or bear_pullback)
            and (bull_confirmation or bear_confirmation)
            and not (
            (bull_setup and buy_breakout)
            or
            (bear_setup and sell_breakout)
        )
    ):
            print("⚠️ Setup Valid But Breakout Not Confirmed")

    print("=" * 65)

    # ======================================
    # BUY
    # ======================================

    if bull_setup and buy_breakout:

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

    # ======================================
    # SELL
    # ======================================

    if bear_setup and sell_breakout:

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

    # ======================================
    # NO TRADE
    # ======================================

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