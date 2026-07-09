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
- Break of Structure (BOS)
- Change of Character (CHOCH)

Future Versions
- Liquidity
- Order Block
"""

from config.strategy import (
    SWING_LOOKBACK,
    BOS_CONFIRMATION_CLOSE,
    BOS_MIN_BREAK_PIPS,
    BOS_MIN_BREAK_ATR,
)

from core.enums import Trend
from strategy.shared.signal import Signal
from strategy.shared.swing import (
    is_swing_high,
    is_swing_low,
    recent_swing_high,
    recent_swing_low,
    get_swing_labels,
)


# ==========================================================
# HELPERS
# ==========================================================

def _get_min_break_size(df):
    """
    Calculate minimum break size in price units based on config.
    Returns 0 if both thresholds are disabled.
    """
    min_size = 0.0
    if BOS_MIN_BREAK_PIPS > 0:
        # Assuming 5-digit pricing; adjust if needed
        point = 0.00001  # placeholder; better to get from symbol info
        min_size = max(min_size, BOS_MIN_BREAK_PIPS * point)
    if BOS_MIN_BREAK_ATR > 0 and "ATR" in df.columns:
        atr_val = df["ATR"].iloc[-1]
        if not pd.isna(atr_val):
            min_size = max(min_size, BOS_MIN_BREAK_ATR * atr_val)
    return min_size


def _price_break(price, level, is_break_above):
    """
    Check if price breaks level considering confirmation method.
    is_break_above: True for break above (close > level), False for break below.
    """
    # For simplicity we implement close-based only; wick-based would need high/low of current candle.
    # We'll ignore wick-based for now and can extend later.
    if is_break_above:
        return price > level
    else:
        return price < level


# ==========================================================
# SETTINGS
# ==========================================================

# SWING_LOOKBACK imported from config


# ==========================================================
# SWING HIGH
# ==========================================================

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


# ==========================================================
# SWING LOW
# ==========================================================

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


# ==========================================================
# FIND ALL SWINGS
# ==========================================================

def get_swing_highs(df):
    """Return list of swing highs as dicts with index and price."""

    swings = []

    for i in range(len(df)):
        if is_swing_high(df, i):
            swings.append({
                "index": i,
                "price": df.iloc[i]["high"]
            })

    return swings


def get_swing_lows(df):
    """Return list of swing lows as dicts with index and price."""

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
    """Return (previous, current) swing high dicts."""

    swings = get_swing_highs(df)

    if len(swings) < 2:
        return None, None

    return swings[-2], swings[-1]


def last_two_swing_lows(df):
    """Return (previous, current) swing low dicts."""

    swings = get_swing_lows(df)

    if len(swings) < 2:
        return None, None

    return swings[-2], swings[-1]


# ==========================================================
# HIGHER HIGH (HH)
# ==========================================================

def higher_high(df):
    """Return True if current swing high > previous swing high."""

    previous, current = last_two_swing_highs(df)

    if previous is None:
        return False

    return current["price"] > previous["price"]


# ==========================================================
# LOWER HIGH (LH)
# ==========================================================

def lower_high(df):
    """Return True if current swing high < previous swing high."""

    previous, current = last_two_swing_highs(df)

    if previous is None:
        return False

    return current["price"] < previous["price"]


# ==========================================================
# HIGHER LOW (HL)
# ==========================================================

def higher_low(df):
    """Return True if current swing low > previous swing low."""

    previous, current = last_two_swing_lows(df)

    if previous is None:
        return False

    return current["price"] > previous["price"]


# ==========================================================
# LOWER LOW (LL)
# ==========================================================

def lower_low(df):
    """Return True if current swing low < previous swing low."""

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
    """Weak bullish structure: either HH or HL."""

    return higher_high(df) or higher_low(df)


def weak_bearish_structure(df):
    """Weak bearish structure: either LH or LL."""

    return lower_high(df) or lower_low(df)


# ==========================================================
# STRUCTURE SCORE
# ==========================================================

def structure_score(df):
    """
    Simple structure score: +1 for HH, +1 for HL, -1 for LH, -1 for LL.
    Range -2 to +2.
    """

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
    2. Close breaks above previous Swing High (with optional confirmation and min size)
    """

    if not bullish_structure(df):
        return False

    previous, current = last_two_swing_highs(df)

    if previous is None:
        return False

    last_close = df.iloc[-1]["close"]
    level = current["price"]

    # Check break direction
    if not _price_break(last_close, level, True):
        return False

    # Check minimum size
    min_size = _get_min_break_size(df)
    if min_size > 0:
        if abs(last_close - level) < min_size:
            return False

    return True


def bearish_bos(df):
    """
    Bearish Break Of Structure

    Requirements
    1. Bearish Structure already exists
    2. Close breaks below previous Swing Low (with optional confirmation and min size)
    """

    if not bearish_structure(df):
        return False

    previous, current = last_two_swing_lows(df)

    if previous is None:
        return False

    last_close = df.iloc[-1]["close"]
    level = current["price"]

    # Check break direction
    if not _price_break(last_close, level, False):
        return False

    # Check minimum size
    min_size = _get_min_break_size(df)
    if min_size > 0:
        if abs(last_close - level) < min_size:
            return False

    return True


# ==========================================================
# CHANGE OF CHARACTER (CHOCH)
# ==========================================================

def bullish_choch(df):
    """
    Bullish Change Of Character
    (Change from bearish to bullish structure)

    Requirements
    1. Bearish Structure already exists
    2. Close breaks above previous Swing Low (break of LL)
    """

    if not bearish_structure(df):
        return False

    previous, current = last_two_swing_lows(df)

    if previous is None:
        return False

    last_close = df.iloc[-1]["close"]
    level = current["price"]

    if not _price_break(last_close, level, True):
        return False

    min_size = _get_min_break_size(df)
    if min_size > 0:
        if abs(last_close - level) < min_size:
            return False

    return True


def bearish_choch(df):
    """
    Bearish Change Of Character
    (Change from bullish to bearish structure)

    Requirements
    1. Bullish Structure already exists
    2. Close breaks below previous Swing High (break of HH)
    """

    if not bullish_structure(df):
        return False

    previous, current = last_two_swing_highs(df)

    if previous is None:
        return False

    last_close = df.iloc[-1]["close"]
    level = current["price"]

    if not _price_break(last_close, level, False):
        return False

    min_size = _get_min_break_size(df)
    if min_size > 0:
        if abs(last_close - level) < min_size:
            return False

    return True


# ==========================================================
# MARKET STRUCTURE API
# ==========================================================

def analyze_market_structure(df):
    """
    Complete Market Structure Analysis

    Returns a dictionary with:
        - Trend (BULLISH/BEARISH/SIDEWAYS)
        - Swing points (HH, HL, LH, LL)
        - Structure flags (bullish_structure, bearish_structure)
        - BOS flags (bullish_bos, bearish_bos)
        - CHOCH flags (bullish_choch, bearish_choch)
        - Structure score
    """

    hh = higher_high(df)
    hl = higher_low(df)
    lh = lower_high(df)
    ll = lower_low(df)

    bullish = hh and hl
    bearish = lh and ll

    bull_bos = False
    bear_bos = False
    bull_choch = False
    bear_choch = False

    if bullish:
        bull_bos = bullish_bos(df)
    if bearish:
        bear_bos = bearish_bos(df)

    # Only check CHOCH when structure is not strongly bullish/bearish
    if not bullish and not bearish:
        bull_choch = bullish_choch(df)
        bear_choch = bearish_choch(df)

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
        # CHOCH
        "bullish_choch": bull_choch,
        "bearish_choch": bear_choch,
        # Score
        "score": score
    }


# ==========================================================
# SIGNAL GENERATORS (Phase 1 Implementation)
# ==========================================================

import pandas as pd  # needed for _get_min_break_size


def get_market_structure_signal(df):
    """
    Generate a Signal for current market structure state.
    """
    analysis = analyze_market_structure(df)
    trend = analysis["trend"]
    score = abs(analysis["score"])

    # Determine direction based on trend
    direction = "NEUTRAL"
    if trend == Trend.BULLISH:
        direction = "BUY"
    elif trend == Trend.BEARISH:
        direction = "SELL"
    elif trend == Trend.SIDEWAYS:
        direction = "NEUTRAL"

    # Normalize score to 0-100 (score range -2 to +2 -> abs 0-2)
    normalized_score = min(100, score * 50)  # 2 * 50 = 100

    # Build reason string
    reason_parts = []
    if analysis["higher_high"]:
        reason_parts.append("HH")
    if analysis["higher_low"]:
        reason_parts.append("HL")
    if analysis["lower_high"]:
        reason_parts.append("LH")
    if analysis["lower_low"]:
        reason_parts.append("LL")

    reason = f"Structure: {'+'.join(reason_parts) if reason_parts else 'None'} | Trend: {trend.value}"

    return Signal(
        detector="market_structure",
        direction=direction,
        score=normalized_score,
        confidence=70,  # Base confidence for structure
        reason=reason,
        meta=analysis,
        timestamp=int(df.index[-1]) if hasattr(df.index[-1], '__int__') else len(df) - 1,
        weight=1.0
    )


def get_bos_signal(df):
    """
    Generate a Signal for Break Of Structure (BOS) detection.
    """
    analysis = analyze_market_structure(df)

    if analysis["bullish_bos"]:
        direction = "BUY"
        reason = f"Bullish BOS: Close {df.iloc[-1]['close']:.5f} > Swing High {last_two_swing_highs(df)[1]['price']:.5f}"
        score = 85
        confidence = 80
    elif analysis["bearish_bos"]:
        direction = "SELL"
        reason = f"Bearish BOS: Close {df.iloc[-1]['close']:.5f} < Swing Low {last_two_swing_lows(df)[1]['price']:.5f}"
        score = 85
        confidence = 80
    else:
        direction = "NEUTRAL"
        reason = "No BOS detected"
        score = 0
        confidence = 0

    # Get previous swing levels for meta
    prev_high_swing, curr_high_swing = last_two_swing_highs(df)
    prev_low_swing, curr_low_swing = last_two_swing_lows(df)

    meta = analysis.copy()
    meta.update({
        "prev_high_swing": prev_high_swing,
        "curr_high_swing": curr_high_swing,
        "prev_low_swing": prev_low_swing,
        "curr_low_swing": curr_low_swing
    })

    return Signal(
        detector="bos",
        direction=direction,
        score=score,
        confidence=confidence,
        reason=reason,
        meta=meta,
        timestamp=int(df.index[-1]) if hasattr(df.index[-1], '__int__') else len(df) - 1,
        weight=1.0
    )


def get_choch_signal(df):
    """
    Generate a Signal for Change Of Character (CHOCH) detection.
    """
    analysis = analyze_market_structure(df)
    if analysis["bullish_choch"]:
        direction = "BUY"
        reason = f"Bullish CHOCH: Close {df.iloc[-1]['close']:.5f} > Swing Low {last_two_swing_lows(df)[1]['price']:.5f}"
        score = 75
        confidence = 75
    elif analysis["bearish_choch"]:
        direction = "SELL"
        reason = f"Bearish CHOCH: Close {df.iloc[-1]['close']:.5f} < Swing High {last_two_swing_highs(df)[1]['price']:.5f}"
        score = 75
        confidence = 75
    else:
        direction = "NEUTRAL"
        reason = "No CHOCH detected"
        score = 0
        confidence = 0

    meta = analysis.copy()

    return Signal(
        detector="choch",
        direction=direction,
        score=score,
        confidence=confidence,
        reason=reason,
        meta=meta,
        timestamp=int(df.index[-1]) if hasattr(df.index[-1], '__int__') else len(df) - 1,
        weight=1.0
    )