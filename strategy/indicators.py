from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange

import pandas as pd

from config.strategy import (
    FAST_EMA,
    SLOW_EMA,
    RSI_PERIOD,
    ATR_PERIOD
)


_REQUIRED_OHLC_COLUMNS = ("open", "high", "low", "close")


def _validate_ohlc_dataframe(df):
    """
    Validate that the input dataframe includes the required OHLC columns.
    """

    if df is None:
        raise ValueError("DataFrame is required.")

    if not isinstance(df, pd.DataFrame):
        raise TypeError("DataFrame must be a pandas DataFrame.")

    missing_columns = [
        column for column in _REQUIRED_OHLC_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "DataFrame is missing required OHLC columns: "
            + ", ".join(missing_columns)
        )

    return df


def add_indicators(df):
    """
    Add all indicators required by strategies.
    """

    df = _validate_ohlc_dataframe(df)

    # ======================================
    # EMA
    # ======================================

    df[f"EMA{FAST_EMA}"] = EMAIndicator(
        close=df["close"],
        window=FAST_EMA
    ).ema_indicator()

    df[f"EMA{SLOW_EMA}"] = EMAIndicator(
        close=df["close"],
        window=SLOW_EMA
    ).ema_indicator()

    # ======================================
    # RSI
    # ======================================

    df["RSI"] = RSIIndicator(
        close=df["close"],
        window=RSI_PERIOD
    ).rsi()

    # ======================================
    # ATR
    # ======================================

    atr = AverageTrueRange(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        window=ATR_PERIOD
    )

    df["ATR"] = atr.average_true_range()

    return df