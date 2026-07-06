"""
Professional Break Even Engine

Version : 2.0
"""

import MetaTrader5 as mt5

from config import SYMBOL

from live_trading.position_manager import get_position


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

    ticket = position.ticket

    entry = position.price_open

    sl = position.sl

    tp = position.tp

    symbol = position.symbol

    tick = mt5.symbol_info_tick(symbol)

    if tick is None:
        return None

    # BUY Position
    if position.type == mt5.POSITION_TYPE_BUY:

        current_price = tick.bid

        risk = entry - sl

        trigger = entry + (risk * BREAK_EVEN_RR)

        if current_price < trigger:
            return None

        # Already Break Even
        if sl >= entry:
            return None

        new_sl = entry

    # SELL Position
    else:

        current_price = tick.ask

        risk = sl - entry

        trigger = entry - (risk * BREAK_EVEN_RR)

        if current_price > trigger:
            return None

        # Already Break Even
        if sl <= entry:
            return None

        new_sl = entry

    request = {

        "action": mt5.TRADE_ACTION_SLTP,

        "position": ticket,

        "symbol": symbol,

        "sl": new_sl,

        "tp": tp

    }

    result = mt5.order_send(request)

    return result