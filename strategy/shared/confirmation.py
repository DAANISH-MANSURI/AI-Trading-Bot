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

import pandas as pd

from config.strategy import (
    CONFIRMATION_BODY_PERCENT,
    CONFIRMATION_WICK_PERCENT
)
from strategy.candle_patterns import (
    bullish_engulfing,
    bearish_engulfing,
    pin_bar
)


_REQUIRED_COLUMNS = ("open", "high", "low", "close")


def _validate_dataframe(df):
    """
    Validate that the input dataframe contains the required columns.
    """

    if df is None:
        raise ValueError("DataFrame is required.")

    if not isinstance(df, pd.DataFrame):
        raise TypeError("DataFrame must be a pandas DataFrame.")

    missing_columns = [
        column for column in _REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "DataFrame is missing required columns: "
            + ", ".join(missing_columns)
        )

    return df


# ==========================================
# Strong Bullish Candle
# ==========================================

def strong_bullish_candle(df):

    df = _validate_dataframe(df)

    if len(df) < 1:
        return False

    last = df.iloc[-1]

    if pd.isna(last["open"]) or pd.isna(last["high"]) or pd.isna(last["low"]) or pd.isna(last["close"]):
        return False

    candle_range = last["high"] - last["low"]

    if candle_range <= 0:
        return False

    body = abs(last["close"] - last["open"])

    body_percent = body / candle_range

    close_near_high = (

        last["high"] - last["close"]

    ) <= (

        candle_range * CONFIRMATION_WICK_PERCENT

    )

    return (

        last["close"] > last["open"]

        and

        body_percent >= CONFIRMATION_BODY_PERCENT

        and

        close_near_high

    )


# ==========================================
# Strong Bearish Candle
# ==========================================

def strong_bearish_candle(df):

    df = _validate_dataframe(df)

    if len(df) < 1:
        return False

    last = df.iloc[-1]

    if pd.isna(last["open"]) or pd.isna(last["high"]) or pd.isna(last["low"]) or pd.isna(last["close"]):
        return False

    candle_range = last["high"] - last["low"]

    if candle_range <= 0:
        return False

    body = abs(last["close"] - last["open"])

    body_percent = body / candle_range

    close_near_low = (

        last["close"] - last["low"]

    ) <= (

        candle_range * CONFIRMATION_WICK_PERCENT

    )

    return (

        last["close"] < last["open"]

        and

        body_percent >= CONFIRMATION_BODY_PERCENT

        and

        close_near_low

    )


# ==========================================
# BUY Confirmation
# ==========================================

def bullish_confirmation(df):

    df = _validate_dataframe(df)

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

    df = _validate_dataframe(df)

    return (

        bearish_engulfing(df)

        or

        pin_bar(df)

        or

        strong_bearish_candle(df)

    )