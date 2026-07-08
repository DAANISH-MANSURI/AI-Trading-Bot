"""
Professional EMA20 Pullback Engine
"""

import pandas as pd

from config.strategy import (
    PULLBACK_ATR_MULTIPLIER,
    PULLBACK_BODY_PERCENT
)
from strategy.shared.helpers import within_tolerance

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

    touch = within_tolerance(

        last["low"],

        ema20,

        tolerance

    )

    if not touch:
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

    touch = within_tolerance(

        last["high"],

        ema20,

        tolerance

    )

    if not touch:
        return False

    if prev["close"] >= prev["EMA20"]:
        return False

    if last["close"] >= ema20:
        return False

    if not strong_bearish_body(last):
        return False

    return True