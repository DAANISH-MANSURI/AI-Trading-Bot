"""
Trend Detection Engine

EMA Pullback Strategy
"""

import pandas as pd

from config.strategy import TREND_LOOKBACK
from core.enums import Trend


EMA_COLUMN = "EMA20"
_REQUIRED_COLUMNS = ("close", EMA_COLUMN)


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
# EMA Slope
# ==========================================

def ema_rising(df, ema=EMA_COLUMN, bars=TREND_LOOKBACK):

    df = _validate_dataframe(df)

    if len(df) < bars + 1:
        return False

    recent = df[ema].tail(bars + 1).to_numpy()

    for i in range(1, len(recent)):

        if recent[i] <= recent[i - 1]:
            return False

    return True


def ema_falling(df, ema=EMA_COLUMN, bars=TREND_LOOKBACK):

    df = _validate_dataframe(df)

    if len(df) < bars + 1:
        return False

    recent = df[ema].tail(bars + 1).to_numpy()

    for i in range(1, len(recent)):

        if recent[i] >= recent[i - 1]:
            return False

    return True


# ==========================================
# Bullish Trend
# ==========================================

def is_bullish(df):

    df = _validate_dataframe(df)

    if len(df) < 2:
        return False

    last = df.iloc[-1]

    return (

        last["close"] > last["EMA20"]

        and

        ema_rising(df)

    )


# ==========================================
# Bearish Trend
# ==========================================

def is_bearish(df):

    df = _validate_dataframe(df)

    if len(df) < 2:
        return False

    last = df.iloc[-1]

    return (

        last["close"] < last["EMA20"]

        and

        ema_falling(df)

    )


# ==========================================
# Current Trend
# ==========================================

def get_trend(df):

    df = _validate_dataframe(df)

    if is_bullish(df):
        return Trend.BULLISH

    if is_bearish(df):
        return Trend.BEARISH

    return Trend.SIDEWAYS