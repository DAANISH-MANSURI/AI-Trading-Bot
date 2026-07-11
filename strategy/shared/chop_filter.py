"""
Choppiness Filter Module

Provides a function to determine if the market is trending based on
ADX (Average Directional Index). Returns True if trending (ADX >= threshold),
False if choppy or on error.
"""

import pandas as pd
from ta.trend import ADXIndicator

from config.strategy import ADX_PERIOD, ADX_MIN_THRESHOLD
from utils.logger import logger


def is_trending(df: pd.DataFrame) -> bool:
    """
    Determine if the market is trending by checking if ADX is above or equal to
    a threshold.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing at least 'high', 'low', 'close' columns.

    Returns
    -------
    bool
        True if ADX >= ADX_MIN_THRESHOLD (trending, safe to trade),
        False if ADX < threshold (choppy) or on any error/insufficient data.
    """
    try:
        # Validate required columns
        if not all(col in df.columns for col in ["high", "low", "close"]):
            logger.warning(
                "Chop filter: DataFrame missing required OHLC columns; "
                "assuming choppy market (returning False)."
            )
            return False

        # Ensure we have enough rows for the ADX period
        if len(df) < ADX_PERIOD:
            logger.warning(
                f"Chop filter: Insufficient data for ADX calculation "
                f"(need at least {ADX_PERIOD} rows, got {len(df)}); "
                "assuming choppy market (returning False)."
            )
            return False

        # Calculate ADX
        adx_indicator = ADXIndicator(
            high=df["high"], low=df["low"], close=df["close"], window=ADX_PERIOD
        )
        adx_values = adx_indicator.adx()
        latest_adx = adx_values.iloc[-1]

        # If the latest ADX is NaN, treat as not trending
        if pd.isna(latest_adx):
            logger.warning(
                "Chop filter: ADX calculation resulted in NaN; "
                "assuming choppy market (returning False)."
            )
            return False

        return bool(latest_adx >= ADX_MIN_THRESHOLD)
    except Exception as e:
        logger.warning(
            f"Chop filter: Unexpected error during ADX calculation: {e}; "
            "assuming choppy market (returning False)."
        )
        return False