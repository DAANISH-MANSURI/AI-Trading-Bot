"""
Higher Timeframe Bias Module

Provides a function to get the higher‑timeframe trend bias based on whether
the current HTF close is above or below a specified EMA (default 200 EMA).
The result is cached per symbol/timeframe to avoid refetching on every call.
"""

from typing import Dict, Tuple

import pandas as pd
from ta.trend import EMAIndicator

from backtesting.historical_data import get_historical_data
from config.strategy import HTF_EMA_PERIOD
from utils.logger import logger

# Simple cache: {(symbol, htf_timeframe): {"ts": timestamp, "bias": str}}
_htf_cache: Dict[Tuple[str, int], dict] = {}


def get_htf_bias(symbol: str, htf_timeframe: int) -> str:
    """
    Determine higher‑timeframe bias (BULLISH/BEARISH) by comparing the
    latest HTF close with its EMA.

    Parameters
    ----------
    symbol : str
        Trading symbol (e.g., "BTCUSD").
    htf_timeframe : int
        MT5 timeframe constant (e.g., mt5.TIMEFRAME_H4).

    Returns
    -------
    str
        "BULLISH" if close > EMA, "BEARISH" if below, or "UNKNOWN" if data
        is unavailable or an error occurred.
    """
    cache_key = (symbol, htf_timeframe)

    # Try to get the latest completed candle timestamp to see if we need
    # to update the cache.
    try:
        latest_df = get_historical_data(symbol, htf_timeframe, 1)
        if latest_df is None or len(latest_df) == 0:
            # No data available; we cannot determine freshness.
            logger.warning(
                f"HTF data unavailable for {symbol} on timeframe {htf_timeframe}; "
                "returning UNKNOWN bias."
            )
            return "UNKNOWN"
    except Exception as e:
        # If we cannot fetch latest data, log and treat as unavailable.
        logger.warning(
            f"Failed to fetch latest HTF candle for {symbol} on timeframe {htf_timeframe}: {e}; "
            "returning UNKNOWN bias."
        )
        return "UNKNOWN"

    latest_time = latest_df["time"].iloc[0]  # most recent completed candle

    # If we have a cached result for the same timestamp, return it.
    if cache_key in _htf_cache and _htf_cache[cache_key]["ts"] == latest_time:
        return _htf_cache[cache_key]["bias"]

    # Fetch enough candles for a stable EMA calculation.
    num_candles = max(HTF_EMA_PERIOD + 100, 300)
    try:
        df = get_historical_data(symbol, htf_timeframe, num_candles)
    except Exception as e:
        logger.warning(
            f"Failed to fetch sufficient HTF data for {symbol} on timeframe {htf_timeframe}: {e}; "
            "returning UNKNOWN bias."
        )
        return "UNKNOWN"

    if df is None or len(df) < HTF_EMA_PERIOD:
        logger.warning(
            f"Insufficient HTF data for {symbol} on timeframe {htf_timeframe} "
            f"(need at least {HTF_EMA_PERIOD} candles, got {len(df) if df is not None else 0}); "
            "returning UNKNOWN bias."
        )
        return "UNKNOWN"

    # Ensure required columns exist.
    if "close" not in df.columns or "time" not in df.columns:
        logger.warning(
            f"HTF data for {symbol} on timeframe {htf_timeframe} missing required columns; "
            "returning UNKNOWN bias."
        )
        return "UNKNOWN"

    # Calculate EMA.
    try:
        ema_indicator = EMAIndicator(close=df["close"], window=HTF_EMA_PERIOD)
        ema_values = ema_indicator.ema_indicator()
        latest_ema = ema_values.iloc[-1]
        latest_close = df["close"].iloc[-1]
    except Exception as e:
        logger.warning(
            f"EMA calculation failed for {symbol} on timeframe {htf_timeframe}: {e}; "
            "returning UNKNOWN bias."
        )
        return "UNKNOWN"

    # Determine bias.
    bias = "BULLISH" if float(latest_close) > float(latest_ema) else "BEARISH"

    # Update cache with the latest timestamp and bias.
    _htf_cache[cache_key] = {"ts": latest_time, "bias": bias}

    return bias


def get_htf_bias_from_df(htf_df, current_time, htf_ema_period=None):
    """
    Backtest-safe HTF bias — computes bias using only HTF candles that
    closed at or before current_time (prevents look-ahead bias).
    No MT5 calls — operates on a pre-loaded dataframe.
    """
    if htf_ema_period is None:
        htf_ema_period = HTF_EMA_PERIOD

    valid_df = htf_df[htf_df["time"] <= current_time]
    if len(valid_df) < htf_ema_period:
        return "UNKNOWN"

    ema_indicator = EMAIndicator(close=valid_df["close"], window=htf_ema_period)
    latest_ema = ema_indicator.ema_indicator().iloc[-1]
    latest_close = valid_df["close"].iloc[-1]

    if latest_close > latest_ema:
        return "BULLISH"
    elif latest_close < latest_ema:
        return "BEARISH"
    return "UNKNOWN"