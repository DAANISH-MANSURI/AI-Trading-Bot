"""
Fibonacci Retracement & Golden Zone Detection Module

This module detects Fibonacci retracement levels, specifically the Golden Zone (50%-61.8%),
and provides trading signals when price overlaps the Golden Zone with confirmation from
active FVG or S/R zones.

The Golden Zone is only meaningful when it overlaps with an active FVG (same type) or
an active S/R zone (same type). A Golden Zone touch alone produces a weak signal.

The module uses the most recent confirmed BOS (Break of Structure) to identify the
impulsive swing leg for Fibonacci retracement calculation.
"""

import pandas as pd
from strategy.shared.signal import Signal
from strategy.shared.fvg import get_active_fvgs
from strategy.shared.sr_zones import get_active_sr_zones
from strategy.shared.market_structure import get_bos_signal
from config.strategy import (
    FIBONACCI_WEIGHT,
)


def get_fibonacci_signal(df):
    """
    Generate a trading signal based on Fibonacci Golden Zone overlap with FVG/SR zones.
    Returns a Signal object with:
        - direction: "BUY" for bullish Golden Zone with confirmation,
                     "SELL" for bearish Golden Zone with confirmation,
                     "NEUTRAL" otherwise
        - score: 0-100 based on confirmation strength (base 30 for Golden Zone touch,
                 +40 for FVG overlap, +30 for S/R zone overlap)
        - confidence: 0-100 (set equal to score for simplicity; used for logging/meta)
        - reason: human-readable description
        - meta: Fibonacci details (swing points, Golden Zone levels, overlap flags)
        - timestamp: bar index of the signal
        - weight: 1.0 (to be weighted by Confluence Engine)
    """
    # Default neutral signal
    default_signal = Signal(
        detector="fibonacci",
        direction="NEUTRAL",
        score=0,
        confidence=0,
        reason="No Fibonacci Golden Zone signal",
        meta={},
        timestamp=int(df.index[-1]) if hasattr(df.index[-1], '__int__') else len(df) - 1,
        weight=1.0
    )

    # Validate dataframe has required columns
    required_columns = ["open", "high", "low", "close"]
    if not all(col in df.columns for col in required_columns):
        return default_signal

    if len(df) < 10:  # Need sufficient data for swing detection
        return default_signal

    # Get the most recent BOS signal to identify the impulsive swing leg
    bos_signal = get_bos_signal(df)
    if bos_signal.direction == "NEUTRAL":
        # No confirmed BOS, cannot reliably determine impulsive swing
        return default_signal

    # Extract swing points from BOS signal meta
    meta = bos_signal.meta
    if bos_signal.direction == "BUY":  # Bullish BOS
        # Bullish BOS: we broke above the current swing high in a bullish structure
        # Impulsive leg: from previous swing low to current swing high
        if "prev_low_swing" not in meta or "curr_high_swing" not in meta:
            return default_signal
        swing_low_price = meta["prev_low_swing"]["price"]
        swing_high_price = meta["curr_high_swing"]["price"]
        swing_type = "bullish"
    else:  # Bearish BOS
        # Bearish BOS: we broke below the current swing low in a bearish structure
        # Impulsive leg: from previous swing high to current swing low
        if "prev_high_swing" not in meta or "curr_low_swing" not in meta:
            return default_signal
        swing_high_price = meta["prev_high_swing"]["price"]
        swing_low_price = meta["curr_low_swing"]["price"]
        swing_type = "bearish"

    # Calculate Golden Zone (50%-61.8% retracement)
    swing_range = swing_high_price - swing_low_price
    if swing_range <= 0:
        return default_signal

    golden_low = swing_low_price + 0.5 * swing_range
    golden_high = swing_low_price + 0.618 * swing_range

    # Get last two candles for touch detection
    last = df.iloc[-1]
    prev = df.iloc[-2]

    # Check if price is touching the Golden Zone (current candle overlaps, previous does not)
    current_overlap = (last["low"] <= golden_high and last["high"] >= golden_low)
    prev_overlap = (prev["low"] <= golden_high and prev["high"] >= golden_low)

    if not (current_overlap and not prev_overlap):
        # Not a fresh touch of the Golden Zone
        return default_signal

    # Base score for touching the Golden Zone
    score = 30

    # Check for overlap with active FVG (same type)
    overlap_fvg = False
    try:
        active_fvgs = get_active_fvgs(df)
        for fvg in active_fvgs:
            if fvg["type"] == ("bullish" if swing_type == "bullish" else "bearish"):
                # Check overlap between Golden Zone and FVG gap
                if (golden_low <= fvg["gap_high"] and golden_high >= fvg["gap_low"]):
                    overlap_fvg = True
                    break
    except Exception:
        pass  # Fail silently on FVG check

    # Check for overlap with active S/R zone (same type)
    overlap_sr = False
    try:
        active_sr_zones = get_active_sr_zones(df)
        for zone in active_sr_zones:
            # Determine zone type: support for bullish swing, resistance for bearish swing
            expected_zone_type = "support" if swing_type == "bullish" else "resistance"
            if zone["type"] == expected_zone_type:
                # Check overlap between Golden Zone and S/R zone
                if (golden_low <= zone["zone_high"] and golden_high >= zone["zone_low"]):
                    overlap_sr = True
                    break
    except Exception:
        pass  # Fail silently on SR zone check

    # Add confirmation scores
    if overlap_fvg:
        score += 40
    if overlap_sr:
        score += 30

    # Cap score at 100
    score = min(100, score)

    # Determine direction based on swing type
    direction = "BUY" if swing_type == "bullish" else "SELL"

    # Prepare reason string
    reason_parts = [f"Golden Zone ({golden_low:.5f}-{golden_high:.5f}) touch"]
    if overlap_fvg:
        reason_parts.append("bullish FVG overlap" if swing_type == "bullish" else "bearish FVG overlap")
    if overlap_sr:
        reason_parts.append("support zone overlap" if swing_type == "bullish" else "resistance zone overlap")
    reason = " + ".join(reason_parts)

    # Prepare metadata
    meta = {
        "swing_low": swing_low_price,
        "swing_high": swing_high_price,
        "golden_zone_low": golden_low,
        "golden_zone_high": golden_high,
        "overlap_fvg": overlap_fvg,
        "overlap_sr": overlap_sr,
        "swing_type": swing_type,
        "bos_direction": bos_signal.direction
    }

    timestamp = int(df.index[-1]) if hasattr(df.index[-1], '__int__') else len(df) - 1

    return Signal(
        detector="fibonacci",
        direction=direction,
        score=score,
        confidence=score,  # Set equal to score for simplicity
        reason=reason,
        meta=meta,
        timestamp=timestamp,
        weight=1.0
    )