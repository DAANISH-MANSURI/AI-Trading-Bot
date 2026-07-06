from config.strategy import SWING_LOOKBACK


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