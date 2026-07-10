"""
Strategy Stop Loss Engine

Calculates stop loss based on market structure with fallback to ATR-based and fixed pip methods.
"""

from core.enums import Signal
from strategy.shared.market_structure import get_swing_lows, get_swing_highs
from mt5.symbol_info import (
    get_stop_level,
    get_point,
    get_digits
)
from config.strategy import (
    ATR_SL_MULTIPLIER,
    FALLBACK_SL_PIPS,
    #POINT_VALUE  # We'll need to define this or use get_point
)


# Note: We assume ATR_SL_MULTIPLIER and FALLBACK_SL_PIPS are added to config/strategy.py
# If not available, we'll use defaults
try:
    from config.strategy import ATR_SL_MULTIPLIER
except ImportError:
    ATR_SL_MULTIPLIER = 1.5

try:
    from config.strategy import FALLBACK_SL_PIPS
except ImportError:
    FALLBACK_SL_PIPS = 20  # Default 20 pips

LOOKBACK = 10  # For backward compatibility with existing swing functions if needed


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def _get_atr_value(df):
    """Get ATR value from dataframe, return 0 if not available."""
    if 'ATR' in df.columns and not pd.isna(df.iloc[-1]['ATR']):
        return float(df.iloc[-1]['ATR'])
    return 0.0


def _get_point_value():
    """Get point value for the current symbol."""
    return get_point()


def _get_pip_value(pips):
    """Convert pips to price units."""
    return pips * _get_point_value()


# ==========================================
# STRUCTURE-BASED STOP LOSS
# ==========================================

def buy_stop_loss(df):
    """
    Calculate stop loss for BUY trade using structure-based method with fallbacks.
    Priority:
    1. Structure-based: recent swing_low - (ATR_SL_MULTIPLIER * ATR)
    2. ATR-based: entry - (ATR_SL_MULTIPLIER * ATR)  [if no swing point]
    3. Fixed pip: entry - (FALLBACK_SL_PIPS in price units)  [if ATR unavailable]
    """
    entry = float(df.iloc[-1]['close'])
    atr = _get_atr_value(df)

    # Get recent swing low
    swing_lows = get_swing_lows(df)
    if swing_lows and len(swing_lows) > 0:
        recent_swing_low = float(swing_lows[-1]['price'])
        # Structure-based SL
        sl_structure = recent_swing_low - (atr * ATR_SL_MULTIPLIER)
        # Ensure SL is below entry
        if sl_structure < entry:
            return sl_structure

    # Fallback 2: ATR-based SL (if no swing point or structure-based invalid)
    if atr > 0:
        sl_atr = entry - (atr * ATR_SL_MULTIPLIER)
        if sl_atr < entry:
            return sl_atr

    # Fallback 3: Fixed pip SL
    sl_fixed = entry - _get_pip_value(FALLBACK_SL_PIPS)
    return sl_fixed


def sell_stop_loss(df):
    """
    Calculate stop loss for SELL trade using structure-based method with fallbacks.
    Priority:
    1. Structure-based: recent swing_high + (ATR_SL_MULTIPLIER * ATR)
    2. ATR-based: entry + (ATR_SL_MULTIPLIER * ATR)  [if no swing point]
    3. Fixed pip: entry + (FALLBACK_SL_PIPS in price units)  [if ATR unavailable]
    """
    entry = float(df.iloc[-1]['close'])
    atr = _get_atr_value(df)

    # Get recent swing high
    swing_highs = get_swing_highs(df)
    if swing_highs and len(swing_highs) > 0:
        recent_swing_high = float(swing_highs[-1]['price'])
        # Structure-based SL
        sl_structure = recent_swing_high + (atr * ATR_SL_MULTIPLIER)
        # Ensure SL is above entry
        if sl_structure > entry:
            return sl_structure

    # Fallback 2: ATR-based SL (if no swing point or structure-based invalid)
    if atr > 0:
        sl_atr = entry + (atr * ATR_SL_MULTIPLIER)
        if sl_atr > entry:
            return sl_atr

    # Fallback 3: Fixed pip SL
    sl_fixed = entry + _get_pip_value(FALLBACK_SL_PIPS)
    return sl_fixed


# ==========================================
# ATR STOP (Kept for backward compatibility)
# ==========================================

def atr_distance(df):
    """
    Original ATR-based stop loss distance calculation.
    Kept for backward compatibility.
    """
    atr = _get_atr_value(df)
    broker = get_stop_level() * get_point()
    return max(atr * ATR_SL_MULTIPLIER, broker)


# ==========================================
# SIMPLE SWINGS (Kept for backward compatibility)
# ==========================================

def recent_swing_low(df):
    """Return recent swing low for backward compatibility."""
    return df["low"].tail(LOOKBACK).min()


def recent_swing_high(df):
    """Return recent swing high for backward compatibility."""
    return df["high"].tail(LOOKBACK).max()


# ==========================================
# MAIN
# ==========================================

def calculate_sl_tp(df, signal):
    """
    Calculate stop loss and take profit for a trade.
    Uses structure-based SL with fallbacks, and fixed RR for TP.
    """
    entry = df.iloc[-1]["close"]

    if signal == Signal.BUY:
        sl = buy_stop_loss(df)
        risk = entry - sl
        tp = entry + (risk * 2.0)  # Using fixed RR of 2.0 for backward compatibility
        # Note: In a fully updated system, RR should come from config

    elif signal == Signal.SELL:
        sl = sell_stop_loss(df)
        risk = sl - entry
        tp = entry - (risk * 2.0)  # Using fixed RR of 2.0 for backward compatibility

    else:
        return None, None

    return (
        round(sl, get_digits()),
        round(tp, get_digits())
    )