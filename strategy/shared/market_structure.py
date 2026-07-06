"""
Professional Market Structure Engine

Version : 1.0

This module detects:

- Swing High
- Swing Low
- Higher High (HH)
- Higher Low (HL)
- Lower High (LH)
- Lower Low (LL)

Future Versions

- BOS
- CHoCH
- Liquidity
- Order Block
"""

from core.enums import Trend


# ==========================================================
# SETTINGS
# ==========================================================

SWING_LOOKBACK = 2


# ==========================================================
# SWING HIGH
# ==========================================================

def is_swing_high(df, index, lookback=SWING_LOOKBACK):

    if index < lookback:
        return False

    if index >= len(df) - lookback:
        return False

    high = df.iloc[index]["high"]

    # Left
    for i in range(index - lookback, index):

        if df.iloc[i]["high"] >= high:
            return False

    # Right
    for i in range(index + 1, index + lookback + 1):

        if df.iloc[i]["high"] > high:
            return False

    return True


# ==========================================================
# SWING LOW
# ==========================================================

def is_swing_low(df, index, lookback=SWING_LOOKBACK):

    if index < lookback:
        return False

    if index >= len(df) - lookback:
        return False

    low = df.iloc[index]["low"]

    # Left
    for i in range(index - lookback, index):

        if df.iloc[i]["low"] <= low:
            return False

    # Right
    for i in range(index + 1, index + lookback + 1):

        if df.iloc[i]["low"] < low:
            return False

    return True


# ==========================================================
# FIND ALL SWINGS
# ==========================================================

def get_swing_highs(df):

    swings = []

    for i in range(len(df)):

        if is_swing_high(df, i):

            swings.append({

                "index": i,

                "price": df.iloc[i]["high"]

            })

    return swings


def get_swing_lows(df):

    swings = []

    for i in range(len(df)):

        if is_swing_low(df, i):

            swings.append({

                "index": i,

                "price": df.iloc[i]["low"]

            })

    return swings

# ==========================================================
# LAST TWO SWINGS
# ==========================================================

def last_two_swing_highs(df):

    swings = get_swing_highs(df)

    if len(swings) < 2:
        return None, None

    return swings[-2], swings[-1]


def last_two_swing_lows(df):

    swings = get_swing_lows(df)

    if len(swings) < 2:
        return None, None

    return swings[-2], swings[-1]


# ==========================================================
# HIGHER HIGH (HH)
# ==========================================================

def higher_high(df):

    previous, current = last_two_swing_highs(df)

    if previous is None:
        return False

    return current["price"] > previous["price"]


# ==========================================================
# LOWER HIGH (LH)
# ==========================================================

def lower_high(df):

    previous, current = last_two_swing_highs(df)

    if previous is None:
        return False

    return current["price"] < previous["price"]


# ==========================================================
# HIGHER LOW (HL)
# ==========================================================

def higher_low(df):

    previous, current = last_two_swing_lows(df)

    if previous is None:
        return False

    return current["price"] > previous["price"]


# ==========================================================
# LOWER LOW (LL)
# ==========================================================

def lower_low(df):

    previous, current = last_two_swing_lows(df)

    if previous is None:
        return False

    return current["price"] < previous["price"]

# ==========================================================
# STRUCTURE STRENGTH
# ==========================================================

def bullish_structure(df):
    """
    Strong Bullish Market Structure

    Conditions

    HH = Higher High
    HL = Higher Low
    """

    hh = higher_high(df)
    hl = higher_low(df)

    return hh and hl


def bearish_structure(df):
    """
    Strong Bearish Market Structure

    Conditions

    LH = Lower High
    LL = Lower Low
    """

    lh = lower_high(df)
    ll = lower_low(df)

    return lh and ll


# ==========================================================
# WEAK STRUCTURE
# ==========================================================

def weak_bullish_structure(df):

    return (

        higher_high(df)

        or

        higher_low(df)

    )


def weak_bearish_structure(df):

    return (

        lower_high(df)

        or

        lower_low(df)

    )


# ==========================================================
# STRUCTURE SCORE
# ==========================================================

def structure_score(df):

    score = 0

    if higher_high(df):
        score += 1

    if higher_low(df):
        score += 1

    if lower_high(df):
        score -= 1

    if lower_low(df):
        score -= 1

    return score

# ==========================================================
# BREAK OF STRUCTURE (BOS)
# ==========================================================

def bullish_bos(df):
    """
    Bullish Break Of Structure

    Requirements

    1. Bullish Structure already exists
    2. Close breaks above previous Swing High
    """

    if not bullish_structure(df):
        return False

    previous, current = last_two_swing_highs(df)

    if previous is None:
        return False

    last_close = df.iloc[-1]["close"]

    return last_close > current["price"]


def bearish_bos(df):
    """
    Bearish Break Of Structure

    Requirements

    1. Bearish Structure already exists
    2. Close breaks below previous Swing Low
    """

    if not bearish_structure(df):
        return False

    previous, current = last_two_swing_lows(df)

    if previous is None:
        return False

    last_close = df.iloc[-1]["close"]

    return last_close < current["price"]

# ==========================================================
# MARKET STRUCTURE API
# ==========================================================

def analyze_market_structure(df):
    """
    Complete Market Structure Analysis

    Returns one dictionary that can be reused
    by every strategy.
    """

    hh = higher_high(df)
    hl = higher_low(df)

    lh = lower_high(df)
    ll = lower_low(df)

    bullish = hh and hl
    bearish = lh and ll

    bull_bos = False
    bear_bos = False

    if bullish:
        bull_bos = bullish_bos(df)

    if bearish:
        bear_bos = bearish_bos(df)

    score = 0

    if hh:
        score += 1

    if hl:
        score += 1

    if lh:
        score -= 1

    if ll:
        score -= 1

    if bullish:
        trend = Trend.BULLISH

    elif bearish:
        trend = Trend.BEARISH

    else:
        trend = Trend.SIDEWAYS

    return {

        # Trend
        "trend": trend,

        # Swings
        "higher_high": hh,
        "higher_low": hl,
        "lower_high": lh,
        "lower_low": ll,

        # Structure
        "bullish_structure": bullish,
        "bearish_structure": bearish,

        # BOS
        "bullish_bos": bull_bos,
        "bearish_bos": bear_bos,

        # Score
        "score": score

    }