"""
Professional Break Even Engine

Version : 2.0
"""

from live_trading.position_manager import (
    get_position,
    get_position_type
)


# ==========================================================
# SETTINGS
# ==========================================================

BREAK_EVEN_RR = 1.0


# ==========================================================
# MOVE SL TO ENTRY
# ==========================================================

def move_to_break_even():

    position = get_position()

    if position is None:
        return None

    entry = position.price_open

    sl = position.sl

    position_type = get_position_type()

    current_price = getattr(position, "price_current", None)

    if current_price is None:
        current_price = getattr(position, "price_open", None)

    if current_price is None:
        return None

    # BUY Position
    if position_type == "BUY":

        risk = entry - sl

        trigger = entry + (risk * BREAK_EVEN_RR)

        if current_price < trigger:
            return None

        # Already Break Even
        if sl >= entry:
            return None

        new_sl = entry

    # SELL Position
    elif position_type == "SELL":

        risk = sl - entry

        trigger = entry - (risk * BREAK_EVEN_RR)

        if current_price > trigger:
            return None

        # Already Break Even
        if sl <= entry:
            return None

        new_sl = entry

    else:
        return None

    return {
        "should_move": True,
        "new_sl": new_sl
    }