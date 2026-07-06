"""
Confirmation Engine

Bullish:
- Bullish Engulfing
- Hammer
- Strong Bullish Candle

Bearish:
- Bearish Engulfing
- Shooting Star
- Strong Bearish Candle
"""

from strategy.candle_patterns import (
    bullish_engulfing,
    bearish_engulfing,
    pin_bar
)


# ==========================================
# Strong Bullish Candle
# ==========================================

def strong_bullish_candle(df):

    last = df.iloc[-1]

    candle_range = last["high"] - last["low"]

    if candle_range == 0:
        return False

    body = abs(last["close"] - last["open"])

    body_percent = body / candle_range

    close_near_high = (

        last["high"] - last["close"]

    ) <= (

        candle_range * 0.20

    )

    return (

        last["close"] > last["open"]

        and

        body_percent >= 0.60

        and

        close_near_high

    )


# ==========================================
# Strong Bearish Candle
# ==========================================

def strong_bearish_candle(df):

    last = df.iloc[-1]

    candle_range = last["high"] - last["low"]

    if candle_range == 0:
        return False

    body = abs(last["close"] - last["open"])

    body_percent = body / candle_range

    close_near_low = (

        last["close"] - last["low"]

    ) <= (

        candle_range * 0.20

    )

    return (

        last["close"] < last["open"]

        and

        body_percent >= 0.60

        and

        close_near_low

    )


# ==========================================
# BUY Confirmation
# ==========================================

def bullish_confirmation(df):

    return (

        bullish_engulfing(df)

        or

        pin_bar(df)

        or

        strong_bullish_candle(df)

    )


# ==========================================
# SELL Confirmation
# ==========================================

def bearish_confirmation(df):

    return (

        bearish_engulfing(df)

        or

        pin_bar(df)

        or

        strong_bearish_candle(df)

    )