from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange

from config.strategy import (
    FAST_EMA,
    SLOW_EMA,
    RSI_PERIOD,
    ATR_PERIOD
)


def add_indicators(df):
    """
    Add all indicators required by strategies.
    """

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