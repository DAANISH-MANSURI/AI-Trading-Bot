import MetaTrader5 as mt5

from config import (
    SYMBOL,
    MAGIC_NUMBER,
    BREAK_EVEN_TRIGGER
)

from broker_manager import (
    get_point,
    get_filling_mode
)


def move_to_break_even():

    positions = mt5.positions_get(symbol=SYMBOL)

    if positions is None or len(positions) == 0:
        return

    position = positions[0]

    tick = mt5.symbol_info_tick(SYMBOL)

    if tick is None:
        return

    point = get_point()

    trigger = BREAK_EVEN_TRIGGER * point

    # BUY
    if position.type == mt5.POSITION_TYPE_BUY:

        current_price = tick.bid

        profit = current_price - position.price_open

    # SELL
    else:

        current_price = tick.ask

        profit = position.price_open - current_price

    if profit < trigger:
        return

    request = {

        "action": mt5.TRADE_ACTION_SLTP,

        "position": position.ticket,

        "symbol": SYMBOL,

        "sl": position.price_open,

        "tp": position.tp,

        "magic": MAGIC_NUMBER,

        "type_filling": get_filling_mode()

    }

    result = mt5.order_send(request)

    return result