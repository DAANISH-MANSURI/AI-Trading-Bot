"""
Professional ATR Trailing Stop

Version : 2.0
"""

from live_trading.position_manager import (
    get_position,
    get_position_type
)

from mt5.symbol_info import get_digits, get_point

# ==========================================
# SETTINGS
# ==========================================

ATR_MULTIPLIER = 1.5


# ==========================================
# ATR TRAILING STOP
# ==========================================

def trailing_stop(df):

    position = get_position()

    if position is None:
        return None

    atr = df.iloc[-1]["ATR"]

    position_type = get_position_type()

    current_price = getattr(position, "price_current", None)

    if current_price is None:
        current_price = getattr(position, "price_open", None)

    if current_price is None:
        return None

    point = get_point()

    # BUY
    if position_type == "BUY":

        new_sl = current_price - (atr * ATR_MULTIPLIER)

        # Never move SL backward
        if new_sl <= position.sl + point:
            return None

    # SELL
    elif position_type == "SELL":

        new_sl = current_price + (atr * ATR_MULTIPLIER)

        # Never move SL backward
        if new_sl >= position.sl - point:
            return None

    else:
        return None

    return {
        "should_trail": True,
        "new_sl": round(new_sl, get_digits())
    }