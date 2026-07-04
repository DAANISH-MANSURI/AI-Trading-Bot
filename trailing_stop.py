import MetaTrader5 as mt5

from config import (
    SYMBOL,
    MAGIC_NUMBER,
    TRAILING_ATR_MULTIPLIER,
    TRAILING_START_ATR
)

from broker_manager import (
    get_digits,
    get_point,
    get_filling_mode
)


def trailing_stop(atr):

    positions = mt5.positions_get(symbol=SYMBOL)

    if positions is None or len(positions) == 0:
        return

    position = positions[0]

    tick = mt5.symbol_info_tick(SYMBOL)

    if tick is None:
        return

    point = get_point()
    digits = get_digits()

    # ============================
    # BUY POSITION
    # ============================

    if position.type == mt5.POSITION_TYPE_BUY:

        current_price = tick.bid

        profit = current_price - position.price_open

        if profit < atr * TRAILING_START_ATR:
            return

        new_sl = current_price - atr * TRAILING_ATR_MULTIPLIER

        # Already Trailing
        if abs(position.sl - new_sl) < point:
            return

        if new_sl <= position.sl:
            return

    # ============================
    # SELL POSITION
    # ============================

    else:

        current_price = tick.ask

        profit = position.price_open - current_price

        if profit < atr * TRAILING_START_ATR:
            return

        new_sl = current_price + atr * TRAILING_ATR_MULTIPLIER

        if position.sl != 0:

            if abs(position.sl - new_sl) < point:
                return

            if new_sl >= position.sl:
                return

    request = {

        "action": mt5.TRADE_ACTION_SLTP,
        "position": position.ticket,
        "symbol": SYMBOL,
        "sl": round(new_sl, digits),
        "tp": position.tp,
        "magic": MAGIC_NUMBER,
        "type_filling": get_filling_mode()

    }

    result = mt5.order_send(request)

    return result