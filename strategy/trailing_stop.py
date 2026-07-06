"""
Professional ATR Trailing Stop

Version : 2.0
"""

import MetaTrader5 as mt5

from config import SYMBOL

from live_trading.position_manager import get_position

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

    ticket = position.ticket

    symbol = position.symbol

    tp = position.tp

    tick = mt5.symbol_info_tick(symbol)

    if tick is None:
        return None

    point = mt5.symbol_info(symbol).point

    # BUY
    if position.type == mt5.POSITION_TYPE_BUY:

        current_price = tick.bid

        new_sl = current_price - (atr * ATR_MULTIPLIER)

        # Never move SL backward
        if new_sl <= position.sl + point:
            return None

    # SELL
    else:

        current_price = tick.ask

        new_sl = current_price + (atr * ATR_MULTIPLIER)

        # Never move SL backward
        if new_sl >= position.sl - point:
            return None

    request = {

        "action": mt5.TRADE_ACTION_SLTP,

        "position": ticket,

        "symbol": symbol,

        "sl": round(new_sl, mt5.symbol_info(symbol).digits),

        "tp": tp

    }

    result = mt5.order_send(request)

    return result