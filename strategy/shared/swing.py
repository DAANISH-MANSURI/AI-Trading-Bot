from config.strategy import SWING_LOOKBACK
from core.enums import Signal as SignalEnum


def recent_swing_low(df, lookback=SWING_LOOKBACK):
    """
    Find latest valid swing low.
    """

    lows = df["low"].values

    start = max(2, len(df) - lookback)

    for i in range(len(df) - 3, start, -1):

        if (
            lows[i] < lows[i - 1]
            and lows[i] < lows[i - 2]
            and lows[i] < lows[i + 1]
            and lows[i] < lows[i + 2]
        ):

            return lows[i]

    return df["low"].tail(lookback).min()


def recent_swing_high(df, lookback=SWING_LOOKBACK):
    """
    Find latest valid swing high.
    """

    highs = df["high"].values

    start = max(2, len(df) - lookback)

    for i in range(len(df) - 3, start, -1):

        if (
            highs[i] > highs[i - 1]
            and highs[i] > highs[i - 2]
            and highs[i] > highs[i + 1]
            and highs[i] > highs[i + 2]
        ):

            return highs[i]

    return df["high"].tail(lookback).max()


def recent_swing_label(df, lookback=SWING_LOOKBACK):
    """
    Find latest swing with its label (HH/HL/LH/LL).
    Returns: (label, price, index) where label is "HH", "HL", "LH", or "LL"
    """

    swings = []

    for i in range(len(df)):

        if is_swing_high(df, i, lookback) and is_swing_low(df, i, lookback):
            # Special case where both high and low are swings (rare)
            swings.append((i, "HH", df.iloc[i]["high"], df.iloc[i]["low"]))
        elif is_swing_high(df, i, lookback):
            swings.append((i, "HH", df.iloc[i]["high"], None))
        elif is_swing_low(df, i, lookback):
            swings.append((i, "LL", None, df.iloc[i]["low"]))

    if not swings:
        return None

    return swings[-1]


def is_swing_high(df, index, lookback=SWING_LOOKBACK):
    """Check if price at index is a swing high."""

    if index < lookback:
        return False

    if index >= len(df) - lookback:
        return False

    high = df.iloc[index]["high"]

    # Left comparison (higher)
    for i in range(index - lookback, index):
        if df.iloc[i]["high"] >= high:
            return False

    # Right comparison (higher)
    for i in range(index + 1, index + lookback + 1):
        if i < len(df) and df.iloc[i]["high"] >= high:
            return False

    return True


def is_swing_low(df, index, lookback=SWING_LOOKBACK):
    """Check if price at index is a swing low."""

    if index < lookback:
        return False

    if index >= len(df) - lookback:
        return False

    low = df.iloc[index]["low"]

    # Left comparison (lower)
    for i in range(index - lookback, index):
        if df.iloc[i]["low"] <= low:
            return False

    # Right comparison (lower)
    for i in range(index + 1, index + lookback + 1):
        if i < len(df) and df.iloc[i]["low"] <= low:
            return False

    return True


def get_swing_labels(df, lookback=SWING_LOOKBACK):
    """
    Get labeled swings with structure information.
    Returns: list of dicts with keys: index, label, price, direction
    """

    swings = []

    for i in range(len(df)):
        if is_swing_high(df, i, lookback):
            swings.append({
                "index": i,
                "label": "HH",
                "price": df.iloc[i]["high"],
                "direction": "HIGH"
            })
        elif is_swing_low(df, i, lookback):
            swings.append({
                "index": i,
                "label": "LL",
                "price": df.iloc[i]["low"],
                "direction": "LOW"
            })

    return swings


def get_swing_highs(df, lookback=SWING_LOOKBACK):
    """
    Get all swing high points in the dataframe.
    Returns: list of dicts with keys: index, price
    """

    highs = []

    for i in range(len(df)):
        if is_swing_high(df, i, lookback):
            highs.append({
                "index": i,
                "price": df.iloc[i]["high"]
            })

    return highs


def get_swing_lows(df, lookback=SWING_LOOKBACK):
    """
    Get all swing low points in the dataframe.
    Returns: list of dicts with keys: index, price
    """

    lows = []

    for i in range(len(df)):
        if is_swing_low(df, i, lookback):
            lows.append({
                "index": i,
                "price": df.iloc[i]["low"]
            })

    return lows