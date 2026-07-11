"""
Candlestick pattern detection functions.
Provides reusable, configurable pin bar, engulfing, and doji detectors.
"""

from config.strategy import (
    PIN_BAR_WICK_RATIO,
    PIN_BAR_MAX_BODY_RATIO,
    PIN_BAR_CLOSE_ZONE,
    DOJI_MAX_BODY_RATIO,
)


def bullish_engulfing(df):
    """
    Bullish engulfing pattern.
    Previous candle bearish, current candle bullish and fully engulfs previous body.
    """
    if len(df) < 2:
        return False
    prev = df.iloc[-2]
    curr = df.iloc[-1]

    return (
        prev["close"] < prev["open"]  # previous bearish
        and curr["close"] > curr["open"]  # current bullish
        and curr["open"] <= prev["close"]  # current open <= previous close
        and curr["close"] >= prev["open"]  # current close >= previous open
    )


def bearish_engulfing(df):
    """
    Bearish engulfing pattern.
    Previous candle bullish, current candle bearish and fully engulfs previous body.
    """
    if len(df) < 2:
        return False
    prev = df.iloc[-2]
    curr = df.iloc[-1]

    return (
        prev["close"] > prev["open"]  # previous bullish
        and curr["close"] < curr["open"]  # current bearish
        and curr["open"] >= prev["close"]  # current open >= previous close
        and curr["close"] <= prev["open"]  # current close <= previous open
    )


def doji(df):
    """
    Doji pattern: body is small relative to the entire range.
    Uses DOJI_MAX_BODY_RATIO from config.
    """
    if len(df) < 1:
        return False
    candle = df.iloc[-1]

    body = abs(candle["close"] - candle["open"])
    total = candle["high"] - candle["low"]
    if total == 0:
        return False
    return body / total <= DOJI_MAX_BODY_RATIO


def bullish_pin_bar(df):
    """
    Bullish pin bar (hammer/rejection closing near high).
    - Long lower wick (at least PIN_BAR_WICK_RATIO * body)
    - Small body (body ratio < PIN_BAR_MAX_BODY_RATIO)
    - Close in the upper zone (above low + (1 - PIN_BAR_CLOSE_ZONE) * range)
    """
    if len(df) < 1:
        return False
    candle = df.iloc[-1]
    open_price = candle["open"]
    high = candle["high"]
    low = candle["low"]
    close = candle["close"]

    body = abs(close - open_price)
    rng = high - low
    if rng == 0:
        return False

    body_ratio = body / rng
    lower_wick = min(open_price, close) - low
    upper_wick = high - max(open_price, close)

    # Bullish: long lower wick, small body, close near upper zone
    cond_pin = (
        lower_wick > body * PIN_BAR_WICK_RATIO
        and body_ratio < PIN_BAR_MAX_BODY_RATIO
        and close > open_price  # bullish candle
        and close >= low + (rng * (1.0 - PIN_BAR_CLOSE_ZONE))
    )
    return cond_pin


def bearish_pin_bar(df):
    """
    Bearish pin bar (shooting star/rejection closing near low).
    - Long upper wick (at least PIN_BAR_WICK_RATIO * body)
    - Small body (body ratio < PIN_BAR_MAX_BODY_RATIO)
    - Close in the lower zone (below high - PIN_BAR_CLOSE_ZONE * range)
    """
    if len(df) < 1:
        return False
    candle = df.iloc[-1]
    open_price = candle["open"]
    high = candle["high"]
    low = candle["low"]
    close = candle["close"]

    body = abs(close - open_price)
    rng = high - low
    if rng == 0:
        return False

    body_ratio = body / rng
    lower_wick = min(open_price, close) - low
    upper_wick = high - max(open_price, close)

    # Bearish: long upper wick, small body, close near lower zone
    cond_pin = (
        upper_wick > body * PIN_BAR_WICK_RATIO
        and body_ratio < PIN_BAR_MAX_BODY_RATIO
        and close < open_price  # bearish candle
        and close <= high * (1.0 - PIN_BAR_CLOSE_ZONE)
    )
    return cond_pin