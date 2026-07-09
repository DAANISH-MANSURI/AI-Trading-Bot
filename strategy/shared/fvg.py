"""
Fair Value Gap (FVG) Detection Module

This module detects Fair Value Gaps (FVGs) and provides signals for retracement
to these zones. An FVG is a 3-candle imbalance where there is a gap between
the first candle's extreme and the third candle's opposite extreme.

Bullish FVG: gap between candle1.high and candle3.low (candle3.low > candle1.high)
Bearish FVG: gap between candle3.high and candle1.low (candle3.high < candle1.low)

The module provides:
- Detection of active FVGs (not invalidated, not expired)
- Signal generation for FVG retracement touches
- Helper functions for pullback integration
"""

import pandas as pd
from strategy.shared.signal import Signal
from config.strategy import (
    FVG_MIN_GAP_ATR,
    FVG_MIN_GAP_PIPS,
    FVG_EXPIRY_CANDLES,
    FVG_BODY_FILTER
)


def _get_min_gap_size(df):
    """
    Calculate minimum gap size in price units based on config.
    Returns 0 if both thresholds are disabled.
    """
    min_size = 0.0
    if FVG_MIN_GAP_PIPS > 0:
        # Assuming 5-digit pricing (0.00001 pip); adjust via symbol info if needed
        point = 0.00001
        min_size = max(min_size, FVG_MIN_GAP_PIPS * point)
    if FVG_MIN_GAP_ATR > 0 and "ATR" in df.columns:
        atr_val = df["ATR"].iloc[-1]
        if not pd.isna(atr_val):
            min_size = max(min_size, FVG_MIN_GAP_ATR * atr_val)
    return min_size


def _is_fvg_valid(gap_low, gap_high, fvg_type, start_idx, df):
    """
    Check if an FVG is still valid (not invalidated by price action and not expired).
    """
    # Check expiration
    if (len(df) - 1 - start_idx) > FVG_EXPIRY_CANDLES:
        return False

    # Check invalidation: price closing on the opposite side of the gap
    for i in range(start_idx + 1, len(df)):
        close_price = df.iloc[i]["close"]
        if fvg_type == "bullish":
            # Bullish FVG invalidated if close < gap_low
            if close_price < gap_low:
                return False
        else:  # bearish
            # Bearish FVG invalidated if close > gap_high
            if close_price > gap_high:
                return False
    return True


def get_active_fvgs(df):
    """
    Detect all active FVGs in the dataframe.
    Returns a list of dictionaries with keys:
        - type: 'bullish' or 'bearish'
        - gap_low: lower bound of the gap
        - gap_high: upper bound of the gap
        - start_idx: index of the third candle that formed the FVG
    """
    if len(df) < 3:
        return []

    fvgs = []
    _REQUIRED_COLUMNS = ("open", "high", "low", "close")
    missing_columns = [c for c in _REQUIRED_COLUMNS if c not in df.columns]
    if missing_columns:
        return []

    # Scan for 3-candle patterns
    for i in range(2, len(df)):
        # Bullish FVG: candle3.low > candle1.high
        if df.iloc[i]["low"] > df.iloc[i-2]["high"]:
            # Middle candle body-to-range filter (if enabled)
            if FVG_BODY_FILTER > 0:
                mid_candle = df.iloc[i-1]
                body = abs(mid_candle["close"] - mid_candle["open"])
                candle_range = mid_candle["high"] - mid_candle["low"]
                if candle_range > 0:
                    body_ratio = body / candle_range
                    if body_ratio < FVG_BODY_FILTER:
                        # Skip this FVG if the middle candle's body is too small
                        continue
            gap_low = df.iloc[i-2]["high"]
            gap_high = df.iloc[i]["low"]
            # Only consider if gap meets minimum size
            min_gap = _get_min_gap_size(df)
            if (gap_high - gap_low) < min_gap:
                continue
            if _is_fvg_valid(gap_low, gap_high, "bullish", i, df):
                fvgs.append({
                    "type": "bullish",
                    "gap_low": round(gap_low, 8),
                    "gap_high": round(gap_high, 8),
                    "start_idx": i
                })

        # Bearish FVG: candle3.high < candle1.low
        if df.iloc[i]["high"] < df.iloc[i-2]["low"]:
            # Middle candle body-to-range filter (if enabled)
            if FVG_BODY_FILTER > 0:
                mid_candle = df.iloc[i-1]
                body = abs(mid_candle["close"] - mid_candle["open"])
                candle_range = mid_candle["high"] - mid_candle["low"]
                if candle_range > 0:
                    body_ratio = body / candle_range
                    if body_ratio < FVG_BODY_FILTER:
                        # Skip this FVG if the middle candle's body is too small
                        continue
            gap_low = df.iloc[i]["high"]
            gap_high = df.iloc[i-2]["low"]
            min_gap = _get_min_gap_size(df)
            if (gap_high - gap_low) < min_gap:
                continue
            if _is_fvg_valid(gap_low, gap_high, "bearish", i, df):
                fvgs.append({
                    "type": "bearish",
                    "gap_low": round(gap_low, 8),
                    "gap_high": round(gap_high, 8),
                    "start_idx": i
                })

    # Sort by most recent first
    fvgs.sort(key=lambda x: x["start_idx"], reverse=True)
    return fvgs


def get_fvg_signal(df):
    """
    Generate a trading signal based on FVG retracement.
    Returns a Signal object with:
        - direction: "BUY" for bullish FVG retest, "SELL" for bearish FVG retest, "NEUTRAL" otherwise
        - score: 0-100 based on gap size (ATR-relative) and age (newer = higher score)
        - confidence: 0-100 (set equal to score for simplicity; used for logging/meta)
        - reason: human-readable description
        - meta: FVG details (type, gap levels, age, etc.)
        - timestamp: bar index of the signal
        - weight: 1.0 (to be weighted by Confluence Engine)
    """
    # Default neutral signal
    default_signal = Signal(
        detector="fvg",
        direction="NEUTRAL",
        score=0,
        confidence=0,
        reason="No active FVG retracement",
        meta={},
        timestamp=int(df.index[-1]) if hasattr(df.index[-1], '__int__') else len(df) - 1,
        weight=1.0
    )

    if len(df) < 3:
        return default_signal

    try:
        active_fvgs = get_active_fvgs(df)
        if not active_fvgs:
            return default_signal

        # Get last two candles for touch detection
        last = df.iloc[-1]
        prev = df.iloc[-2]

        # Check for fvgs being touched for the first time (current candle overlaps, previous does not)
        touched_fvgs = []
        for fvg in active_fvgs:
            # Current candle overlap condition
            current_overlap = (last["low"] <= fvg['gap_high'] and
                             last["high"] >= fvg['gap_low'])
            # Previous candle overlap condition
            prev_overlap = (prev["low"] <= fvg['gap_high'] and
                          prev["high"] >= fvg['gap_low'])

            if current_overlap and not prev_overlap:
                touched_fvgs.append(fvg)

        if not touched_fvgs:
            return default_signal

        # Select the most significant touched FVG (largest gap, then most recent)
        def fvg_score(fvg):
            gap_size = fvg['gap_high'] - fvg['gap_low']
            age = (len(df) - 1) - fvg['start_idx']
            # Size score: normalize by ATR, cap at 10 ATRs -> 0-10 range
            atr = df["ATR"].iloc[-1] if "ATR" in df.columns and not pd.isna(df["ATR"].iloc[-1]) else 0.001
            size_score = min(gap_size / atr, 10) if atr > 0 else 0
            # Age score: newer = higher
            age_score = (FVG_EXPIRY_CANDLES - age) / FVG_EXPIRY_CANDLES * 50 if FVG_EXPIRY_CANDLES > 0 else 0
            return size_score * 5 + age_score  # 0-100 range

        best_fvg = max(touched_fvgs, key=fvg_score)
        gap_size = best_fvg['gap_high'] - best_fvg['gap_low']
        atr = df["ATR"].iloc[-1] if "ATR" in df.columns and not pd.isna(df["ATR"].iloc[-1]) else 0.001
        size_score = min(gap_size / atr, 10) if atr > 0 else 0
        age = (len(df) - 1) - best_fvg['start_idx']
        age_score = (FVG_EXPIRY_CANDLES - age) / FVG_EXPIRY_CANDLES * 50 if FVG_EXPIRY_CANDLES > 0 else 0
        score = min(100, max(0, size_score * 5 + age_score))

        # Determine direction and reason
        if best_fvg['type'] == "bullish":
            direction = "BUY"
            reason = f"Bullish FVG retest: gap [{best_fvg['gap_low']:.5f}, {best_fvg['gap_high']:.5f}]"
        else:
            direction = "SELL"
            reason = f"Bearish FVG retest: gap [{best_fvg['gap_low']:.5f}, {best_fvg['gap_high']:.5f}]"

        # Confidence set equal to score (per simplification request)
        confidence = score

        # Prepare metadata
        meta = {
            "fvg_type": best_fvg['type'],
            "gap_low": best_fvg['gap_low'],
            "gap_high": best_fvg['gap_high'],
            "age": age,
            "gap_size": round(gap_size, 8),
            "size_score": round(size_score, 2),
            "age_score": round(age_score, 2)
        }

        timestamp = int(df.index[-1]) if hasattr(df.index[-1], '__int__') else len(df) - 1

        return Signal(
            detector="fvg",
            direction=direction,
            score=round(score, 2),
            confidence=round(confidence, 2),
            reason=reason,
            meta=meta,
            timestamp=timestamp,
            weight=1.0
        )

    except Exception as e:
        # Fail-safe: return neutral signal on any error
        return default_signal