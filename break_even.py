import MetaTrader5 as mt5

from config import (
    SYMBOL,
    MAGIC_NUMBER,
    BREAK_EVEN_TRIGGER,
    DEVIATION
)


def move_to_break_even():

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

        profit_points = (
            current_price - position.price_open
        )

        if profit_points >= BREAK_EVEN_TRIGGER:

            request = {

                "action": mt5.TRADE_ACTION_SLTP,
                "position": position.ticket,
                "symbol": SYMBOL,
                "sl": position.price_open,
                "tp": position.tp,
                "magic": MAGIC_NUMBER

            }

            result = mt5.order_send(request)

            return result

    # SELL Position
    else:

        current_price = tick.ask

        profit_points = (
            position.price_open - current_price
        )

        if profit_points >= 0.0010:

            request = {

                "action": mt5.TRADE_ACTION_SLTP,
                "position": position.ticket,
                "symbol": SYMBOL,
                "sl": position.price_open,
                "tp": position.tp,
                "magic": MAGIC_NUMBER

            }

            result = mt5.order_send(request)

            return result