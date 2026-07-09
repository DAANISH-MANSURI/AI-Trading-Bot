"""
Professional EMA20 Pullback Engine
"""

import pandas as pd

from config.strategy import (
    PULLBACK_ATR_MULTIPLIER,
    PULLBACK_BODY_PERCENT,
    FVG_PULLBACK_TOLERANCE
)
from strategy.shared.helpers import within_tolerance
from strategy.shared.fvg import get_active_fvgs  # Import for FVG integration

_REQUIRED_COLUMNS = ("open", "high", "low", "close", "EMA20", "ATR")


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


def strong_bullish_body(last):

    body = abs(last["close"] - last["open"])

    candle = last["high"] - last["low"]

    if candle == 0:
        return False

    return (

        last["close"] > last["open"]

        and

        body >= candle * PULLBACK_BODY_PERCENT

    )


def strong_bearish_body(last):

    body = abs(last["close"] - last["open"])

    candle = last["high"] - last["low"]

    if candle == 0:
        return False

    return (

        last["close"] < last["open"]

        and

        body >= candle * PULLBACK_BODY_PERCENT

    )


def bullish_pullback(
    df,
    atr_multiplier=PULLBACK_ATR_MULTIPLIER
):

    df = _validate_dataframe(df)

    if len(df) < 2:
        return False

    last = df.iloc[-1]
    prev = df.iloc[-2]

    ema20 = last["EMA20"]
    atr = last["ATR"]

    if pd.isna(atr) or atr <= 0:
        return False

    tolerance = atr * atr_multiplier

    # Existing EMA20 touch condition
    touch_ema = within_tolerance(
        last["low"],
        ema20,
        tolerance
    )

    # New FVG touch condition: check for active bullish FVGs
    try:
        active_fvgs = get_active_fvgs(df)
        bullish_fvgs = [f for f in active_fvgs if f['type'] == 'bullish']
        touch_fvg = False
        for fvg in bullish_fvgs:
            # Check if price is within FVG gap with tolerance
            atr = last["ATR"] if "ATR" in last and not pd.isna(last["ATR"]) else 0.001
            tolerance = atr * FVG_PULLBACK_TOLERANCE

            # Extended gap boundaries with tolerance
            extended_low = fvg['gap_low'] - tolerance
            extended_high = fvg['gap_high'] + tolerance

            # Check if candle overlaps with extended FVG
            if last["high"] >= extended_low and last["low"] <= extended_high:
                touch_fvg = True
                break
    except Exception:
        # If FVG detection fails, fall back to EMA20 only
        touch_fvg = False

    # Combined touch condition: EMA20 OR FVG
    touch_condition = touch_ema or touch_fvg

    if not touch_condition:
        return False

    if prev["close"] <= prev["EMA20"]:
        return False

    if last["close"] <= ema20:
        return False

    if not strong_bullish_body(last):
        return False

    return True


def bearish_pullback(
    df,
    atr_multiplier=PULLBACK_ATR_MULTIPLIER
):

    df = _validate_dataframe(df)

    if len(df) < 2:
        return False

    last = df.iloc[-1]
    prev = df.iloc[-2]

    ema20 = last["EMA20"]
    atr = last["ATR"]

    if pd.isna(atr) or atr <= 0:
        return False

    tolerance = atr * atr_multiplier

    # Existing EMA20 touch condition
    touch_ema = within_tolerance(
        last["high"],
        ema20,
        tolerance
    )

    # New FVG touch condition: check for active bearish FVGs
    try:
        active_fvgs = get_active_fvgs(df)
        bearish_fvgs = [f for f in active_fvgs if f['type'] == 'bearish']
        touch_fvg = False
        for fvg in bearish_fvgs:
            # Check if price is within FVG gap with tolerance
            atr = last["ATR"] if "ATR" in last and not pd.isna(last["ATR"]) else 0.001
            tolerance = atr * FVG_PULLBACK_TOLERANCE

            # Extended gap boundaries with tolerance
            extended_low = fvg['gap_low'] - tolerance
            extended_high = fvg['gap_high'] + tolerance

            # Check if candle overlaps with extended FVG
            if last["high"] >= extended_low and last["low"] <= extended_high:
                touch_fvg = True
                break
    except Exception:
        # If FVG detection fails, fall back to EMA20 only
        touch_fvg = False

    # Combined touch condition: EMA20 OR FVG
    touch_condition = touch_ema or touch_fvg

    if not touch_condition:
        return False

    if prev["close"] >= prev["EMA20"]:
        return False

    if last["close"] >= ema20:
        return False

    if not strong_bearish_body(last):
        return False

    return True