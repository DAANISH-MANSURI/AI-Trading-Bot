"""
EMA 9/20 + Price Action Strategy

Implements a simple state machine based on EMA crossovers, higher timeframe bias,
and trend strength (ADX). This step implements the skeleton and the first two
transitions: IDLE -> WAITING_FOR_PULLBACK on a valid crossover, and
WAITING_FOR_PULLBACK -> IDLE on an invalidating opposite crossover.
"""

from core.enums import Signal, Trend
from typing import Dict, Optional

import pandas as pd
from strategy.shared.htf_bias import get_htf_bias
from strategy.shared.chop_filter import is_trending
from config.strategy import HTF_TIMEFRAME, PULLBACK_ATR_TOLERANCE, PIN_BAR_WICK_RATIO, PIN_BAR_CLOSE_ZONE, PIN_BAR_MAX_BODY_RATIO, DOJI_MAX_BODY_RATIO, MAX_REJECTION_WAIT_CANDLES, BREAKOUT_WAIT_CANDLES
from strategy.candle_patterns import bullish_pin_bar, bearish_pin_bar, bullish_engulfing, bearish_engulfing, doji
from strategy.stop_loss import calculate_sl_tp


# States for the state machine
STATE_IDLE = "IDLE"
STATE_WAITING_FOR_PULLBACK = "WAITING_FOR_PULLBACK"
STATE_WAITING_FOR_REJECTION = "WAITING_FOR_REJECTION"
STATE_WAITING_FOR_BREAKOUT = "WAITING_FOR_BREAKOUT"
STATE_IN_TRADE = "IN_TRADE"

# Module-level state storage: keyed by symbol
_state: Dict[str, dict] = {}  # symbol -> {"state": str, "direction": Optional[str]}


def _get_state(symbol: str) -> dict:
    """Get or initialize state for a symbol."""
    if symbol not in _state:
        _state[symbol] = {
            "state": STATE_IDLE,
            "direction": None,
            "rejection_detected": False,
            "rejection_high": None,
            "rejection_low": None,
            "rejection_wait": 0,
            "breakout_wait": 0,
            "sl": None,
            "tp": None
        }
    return _state[symbol]


def detect_crossover(df) -> Optional[str]:
    """
    Detect EMA9/EMA20 crossover on the last two candles.

    Returns
    -------
    str or None
        "BULLISH_CROSS" if EMA9 crossed above EMA20,
        "BEARISH_CROSS" if EMA9 crossed below EMA20,
        None if no crossover or insufficient data.
    """
    if df is None or len(df) < 2:
        return None

    # Ensure required columns exist (they should be added by indicators.py)
    required = ["EMA9", "EMA20"]
    if not all(col in df.columns for col in required):
        return None

    prev = df.iloc[-2]
    curr = df.iloc[-1]

    prev_fast = prev["EMA9"]
    prev_slow = prev["EMA20"]
    curr_fast = curr["EMA9"]
    curr_slow = curr["EMA20"]

    # Bullish cross: fast was <= slow, now fast > slow
    if prev_fast <= prev_slow and curr_fast > curr_slow:
        return "BULLISH_CROSS"
    # Bearish cross: fast was >= slow, now fast < slow
    if prev_fast >= prev_slow and curr_fast < curr_slow:
        return "BEARISH_CROSS"

    return None


def is_rejection_candle(df: pd.DataFrame, direction: str) -> bool:
    """
    Determine if the last candle is a rejection candle for the given direction.
    Uses configured via strategy.candle_patterns.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with OHLC data.
    direction : str
        Either "BULLISH" or "BEARISH" indicating the expected rejection direction.

    Returns
    -------
    bool
        True if the candle qualifies as a rejection candle.
    """
    if df is None or len(df) < 1:
        return False
    if direction == "BULLISH":
        return bullish_pin_bar(df) or bullish_engulfing(df) or doji(df)
    elif direction == "BEARISH":
        return bearish_pin_bar(df) or bearish_engulfing(df) or doji(df)
    else:
        return False


def get_signal(df):
    """
    Entry point for the EMA 9/20 + Price Action strategy.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with OHLCV data and at least EMA9 and EMA20 columns
        (added by strategy.indicators.add_indicators).

    Returns
    -------
    dict
        Dictionary with keys matching the legacy format for compatibility.
    """
    if df is None or len(df) < 2:
        return {
            "strategy": "EMA 9/20 + Price Action",
            "trend": Trend.SIDEWAYS,
            "signal": Signal.NO_TRADE,
            "confidence": 0,
            "reason": "Not Enough Data",
            "setup_high": None,
            "setup_low": None,
            "entry_price": None,
        }

    symbol = df.attrs.get("symbol", None)
    if symbol is None:
        return {
            "strategy": "EMA 9/20 + Price Action",
            "trend": Trend.SIDEWAYS,
            "signal": Signal.NO_TRADE,
            "confidence": 0,
            "reason": "Symbol not available in dataframe",
            "setup_high": None,
            "setup_low": None,
            "entry_price": None,
        }

    state_info = _get_state(symbol)
    current_state = state_info["state"]
    direction = state_info["direction"]

    crossover = detect_crossover(df)

    # Determine HTF bias and trend strength
    htf_bias = get_htf_bias(symbol, HTF_TIMEFRAME)
    trending = is_trending(df)

    # If we don't have HTF bias or not trending, we cannot consider a crossover valid
    if htf_bias == "UNKNOWN" or not trending:
        # Stay in current state (likely IDLE) and return NO_TRADE
        return {
            "strategy": "EMA 9/20 + Price Action",
            "trend": Trend.SIDEWAYS,
            "signal": Signal.NO_TRADE,
            "confidence": 0,
            "reason": f"HTF bias unknown or not trending (bias={htf_bias}, trending={trending})",
            "setup_high": None,
            "setup_low": None,
            "entry_price": None,
        }

    # Map HTF bias to Trend enum for output
    if htf_bias == "BULLISH":
        htf_trend = Trend.BULLISH
    elif htf_bias == "BEARISH":
        htf_trend = Trend.BEARISH
    else:
        htf_trend = Trend.SIDEWAYS

    # State transitions
    new_state = current_state
    new_direction = direction
    trade_signal = Signal.NO_TRADE
    reason = "No valid setup"
    confidence = 0
    setup_high = None
    setup_low = None
    entry_price = None

    if current_state == STATE_IDLE:
        if crossover == "BULLISH_CROSS" and htf_bias == "BULLISH":
            new_state = STATE_WAITING_FOR_PULLBACK
            new_direction = "BULLISH"
            reason = "Bullish crossover with HTF bias and trend"
            confidence = 70  # placeholder
        elif crossover == "BEARISH_CROSS" and htf_bias == "BEARISH":
            new_state = STATE_WAITING_FOR_PULLBACK
            new_direction = "BEARISH"
            reason = "Bearish crossover with HTF bias and trend"
            confidence = 70  # placeholder
        else:
            reason = "IDLE: waiting for valid crossover"

    elif current_state == STATE_WAITING_FOR_PULLBACK:
        # If we get an opposite crossover, invalidate and go back to IDLE
        if crossover == "BEARISH_CROSS" and direction == "BULLISH":
            new_state = STATE_IDLE
            new_direction = None
            reason = "Invalidating bearish crossover while waiting for bullish pullback"
            confidence = 0
        elif crossover == "BULLISH_CROSS" and direction == "BEARISH":
            new_state = STATE_IDLE
            new_direction = None
            reason = "Invalidating bullish crossover while waiting for bearish pullback"
            confidence = 0
        else:
            # Check for pullback into EMA band
            # Ensure ATR and EMA columns exist
            if all(col in df.columns for col in ["ATR", "EMA9", "EMA20"]):
                atr = df.iloc[-1]["ATR"]
                if not pd.isna(atr) and atr > 0:
                    ema9 = df.iloc[-1]["EMA9"]
                    ema20 = df.iloc[-1]["EMA20"]
                    high = df.iloc[-1]["high"]
                    low = df.iloc[-1]["low"]
                    higher = max(ema9, ema20)
                    lower = min(ema9, ema20)
                    tolerance = PULLBACK_ATR_TOLERANCE * atr
                    if direction == "BULLISH":
                        # price low should be between lower - tolerance and higher
                        if low >= lower - tolerance and low <= higher:
                            new_state = STATE_WAITING_FOR_REJECTION
                            reason = "Pullback detected - price entered EMA band (bullish)"
                            confidence = 60  # placeholder
                    elif direction == "BEARISH":
                        # price high should be between lower and higher + tolerance
                        if high >= lower and high <= higher + tolerance:
                            new_state = STATE_WAITING_FOR_REJECTION
                            reason = "Pullback detected - price entered EMA band (bearish)"
                            confidence = 60  # placeholder
            # If no pullback detected, stay in WAITING_FOR_PULLBACK
            if new_state == STATE_WAITING_FOR_PULLBACK:
                reason = "WAITING_FOR_PULLBACK: waiting for pullback signal"
                confidence = 50  # placeholder

    elif current_state == STATE_WAITING_FOR_REJECTION:
        # Increment wait counter if we haven't detected a rejection yet
        if not state_info["rejection_detected"]:
            state_info["rejection_wait"] += 1
        # Check for opposite crossover (invalidate)
        if crossover:
            if (crossover == "BEARISH_CROSS" and direction == "BULLISH") or \
               (crossover == "BULLISH_CROSS" and direction == "BEARISH"):
                new_state = STATE_IDLE
                new_direction = None
                reason = "Invalidating opposite crossover while waiting for rejection"
                confidence = 0
        # Check timeout
        if state_info["rejection_wait"] >= MAX_REJECTION_WAIT_CANDLES and not state_info["rejection_detected"]:
            # Timed out without rejection, go back to waiting for pullback (same direction)
            new_state = STATE_WAITING_FOR_PULLBACK
            reason = "Rejection wait exceeded, returning to pullback wait"
            confidence = 40  # placeholder
        # Check for rejection candle
        if not state_info["rejection_detected"] and is_rejection_candle(df, direction):
            state_info["rejection_detected"] = True
            state_info["rejection_high"] = float(df.iloc[-1]["high"])
            state_info["rejection_low"] = float(df.iloc[-1]["low"])
            # Transition to WAITING_FOR_BREAKOUT (await breakout)
            new_state = STATE_WAITING_FOR_BREAKOUT
        # Determine reason and confidence if still waiting and not timed out
        if new_state == STATE_WAITING_FOR_REJECTION:
            reason = f"Waiting for rejection candle ({state_info['rejection_wait']}/{MAX_REJECTION_WAIT_CANDLES})"
            confidence = 50  # placeholder
        elif new_state == STATE_WAITING_FOR_BREAKOUT:
            reason = "Rejection detected, awaiting breakout"
            confidence = 70  # placeholder
    elif current_state == STATE_WAITING_FOR_BREAKOUT:
        # Invalidation check first: opposite EMA crossover -> STATE_IDLE
        if crossover:
            if (crossover == "BEARISH_CROSS" and direction == "BULLISH") or \
               (crossover == "BULLISH_CROSS" and direction == "BEARISH"):
                new_state = STATE_IDLE
                new_direction = None
                reason = "Invalidating opposite crossover while waiting for breakout"
                confidence = 0
        else:
            # No opposite crossover, check for breakout
            if direction == "BULLISH":
                if df.iloc[-1]["close"] > state_info["rejection_high"]:
                    # Bullish breakout confirmed - check SL/TP
                    sl, tp = calculate_sl_tp(df, Signal.BUY)
                    if sl is not None and tp is not None:
                        # Both valid, enter trade
                        new_state = STATE_IN_TRADE
                        trade_signal = Signal.BUY
                        entry_price = state_info["rejection_high"]
                        # Store in state for logging
                        state_info["sl"] = sl
                        state_info["tp"] = tp
                        # For the return dict, we'll set setup_high and setup_low to the higher and lower of SL and TP
                        setup_high = max(sl, tp)
                        setup_low = min(sl, tp)
                        reason = "Bullish breakout confirmed"
                        confidence = 80
                    else:
                        # SL/TP calculation failed, treat as no breakout (but we already know price is beyond rejection level)
                        state_info["breakout_wait"] += 1
                        if state_info["breakout_wait"] >= BREAKOUT_WAIT_CANDLES:
                            # Timeout: return to waiting for rejection (same direction)
                            new_state = STATE_WAITING_FOR_REJECTION
                            # Reset rejection-related flags for a fresh start
                            state_info["rejection_detected"] = False
                            state_info["rejection_wait"] = 0
                            state_info["rejection_high"] = None
                            state_info["rejection_low"] = None
                            state_info["breakout_wait"] = 0
                            reason = "Breakout confirmed but SL/TP calculation failed, waiting too long"
                            confidence = 40  # placeholder
                        else:
                            # Still waiting for breakout with valid SL/TP
                            reason = f"Breakout detected but SL/TP calculation failed ({state_info['breakout_wait']}/{BREAKOUT_WAIT_CANDLES})"
                            confidence = 50  # placeholder
                else:
                    # No breakout yet, increment breakout_wait and check timeout
                    state_info["breakout_wait"] += 1
                    if state_info["breakout_wait"] >= BREAKOUT_WAIT_CANDLES:
                        # Timeout: return to waiting for rejection (same direction)
                        new_state = STATE_WAITING_FOR_REJECTION
                        # Reset rejection-related flags for a fresh start
                        state_info["rejection_detected"] = False
                        state_info["rejection_wait"] = 0
                        state_info["rejection_high"] = None
                        state_info["rejection_low"] = None
                        state_info["breakout_wait"] = 0
                        reason = "Breakout waited too long, returning to rejection wait"
                        confidence = 40  # placeholder
                    else:
                        # Still waiting for breakout
                        reason = f"Waiting for breakout ({state_info['breakout_wait']}/{BREAKOUT_WAIT_CANDLES})"
                        confidence = 50  # placeholder
            elif direction == "BEARISH":
                if df.iloc[-1]["close"] < state_info["rejection_low"]:
                    # Bearish breakout confirmed - check SL/TP
                    sl, tp = calculate_sl_tp(df, Signal.SELL)
                    if sl is not None and tp is not None:
                        # Both valid, enter trade
                        new_state = STATE_IN_TRADE
                        trade_signal = Signal.SELL
                        entry_price = state_info["rejection_low"]
                        # Store in state for logging
                        state_info["sl"] = sl
                        state_info["tp"] = tp
                        # For the return dict, we'll set setup_high and setup_low to the higher and lower of SL and TP
                        setup_high = max(sl, tp)
                        setup_low = min(sl, tp)
                        reason = "Bearish breakout confirmed"
                        confidence = 80
                    else:
                        # SL/TP calculation failed, treat as no breakout (but we already know price is beyond rejection level)
                        state_info["breakout_wait"] += 1
                        if state_info["breakout_wait"] >= BREAKOUT_WAIT_CANDLES:
                            # Timeout: return to waiting for rejection (same direction)
                            new_state = STATE_WAITING_FOR_REJECTION
                            # Reset rejection-related flags for a fresh start
                            state_info["rejection_detected"] = False
                            state_info["rejection_wait"] = 0
                            state_info["rejection_high"] = None
                            state_info["rejection_low"] = None
                            state_info["breakout_wait"] = 0
                            reason = "Breakout confirmed but SL/TP calculation failed, waiting too long"
                            confidence = 40  # placeholder
                        else:
                            # Still waiting for breakout with valid SL/TP
                            reason = f"Breakout detected but SL/TP calculation failed ({state_info['breakout_wait']}/{BREAKOUT_WAIT_CANDLES})"
                            confidence = 50  # placeholder
                else:
                    # No breakout yet, increment breakout_wait and check timeout
                    state_info["breakout_wait"] += 1
                    if state_info["breakout_wait"] >= BREAKOUT_WAIT_CANDLES:
                        # Timeout: return to waiting for rejection (same direction)
                        new_state = STATE_WAITING_FOR_REJECTION
                        # Reset rejection-related flags for a fresh start
                        state_info["rejection_detected"] = False
                        state_info["rejection_wait"] = 0
                        state_info["rejection_high"] = None
                        state_info["rejection_low"] = None
                        state_info["breakout_wait"] = 0
                        reason = "Breakout waited too long, returning to rejection wait"
                        confidence = 40  # placeholder
                    else:
                        # Still waiting for breakout
                        reason = f"Waiting for breakout ({state_info['breakout_wait']}/{BREAKOUT_WAIT_CANDLES})"
                        confidence = 50  # placeholder
    elif current_state == STATE_IN_TRADE:
        # Check for exit condition: EMA cross-back
        exit_signal = None
        if crossover:
            if direction == "BULLISH" and crossover == "BEARISH_CROSS":
                exit_signal = Signal.EXIT_BUY
            elif direction == "BEARISH" and crossover == "BULLISH_CROSS":
                exit_signal = Signal.EXIT_SELL
        if exit_signal is not None:
            # Exit the trade
            new_state = STATE_IDLE
            new_direction = None
            trade_signal = exit_signal
            reason = "EMA cross-back exit"
            confidence = 0
            # Reset state fields
            state_info["direction"] = None
            state_info["rejection_detected"] = False
            state_info["rejection_high"] = None
            state_info["rejection_low"] = None
            state_info["rejection_wait"] = 0
            state_info["breakout_wait"] = 0
            state_info["sl"] = None
            state_info["tp"] = None
            # Clear setup_high and setup_low in the return dict
            setup_high = None
            setup_low = None
        else:
            # No exit signal, stay in trade
            reason = "Already in trade"
            confidence = 0
            new_state = current_state  # stay in IN_TRADE
            new_direction = direction  # keep direction
            # Keep setup_high and setup_low as they are (from entry)
    else:
        # Should not happen, but if so, return NO_TRADE
        reason = f"Unknown state {current_state}"
        confidence = 0

    # Update state
    state_info["state"] = new_state
    state_info["direction"] = new_direction

    return {
        "strategy": "EMA 9/20 + Price Action",
        "trend": htf_trend,
        "signal": trade_signal,
        "confidence": confidence,
        "reason": reason,
        "setup_high": setup_high,
        "setup_low": setup_low,
        "entry_price": entry_price,
    }