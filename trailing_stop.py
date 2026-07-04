import MetaTrader5 as mt5

from config import (
    SYMBOL,
    MAGIC_NUMBER,
    TRAILING_ATR_MULTIPLIER,
    TRAILING_START_ATR
)


def trailing_stop(atr):

    positions = mt5.positions_get(symbol=SYMBOL)

    if positions is None:
        return

    if len(positions) == 0:
        return

    position = positions[0]

    tick = mt5.symbol_info_tick(SYMBOL)

    if tick is None:
        return

    # BUY Position
    if position.type == mt5.POSITION_TYPE_BUY:

        current_price = tick.bid

        profit = current_price - position.price_open

        if profit >= atr * TRAILING_START_ATR:

            new_sl = current_price - atr * TRAILING_ATR_MULTIPLIER

            if new_sl > position.sl:

                request = {

                    "action": mt5.TRADE_ACTION_SLTP,
                    "position": position.ticket,
                    "symbol": SYMBOL,
                    "sl": round(new_sl, 5),
                    "tp": position.tp,
                    "magic": MAGIC_NUMBER

                }

                return mt5.order_send(request)

    # SELL Position
    else:

        current_price = tick.ask

        profit = position.price_open - current_price

        if profit >= atr * TRAILING_START_ATR:

            new_sl = current_price + atr * TRAILING_ATR_MULTIPLIER

            if position.sl == 0 or new_sl < position.sl:

                request = {

                    "action": mt5.TRADE_ACTION_SLTP,
                    "position": position.ticket,
                    "symbol": SYMBOL,
                    "sl": round(new_sl, 5),
                    "tp": position.tp,
                    "magic": MAGIC_NUMBER

                }

                return mt5.order_send(request)