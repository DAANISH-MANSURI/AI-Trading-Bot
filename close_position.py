import MetaTrader5 as mt5

from config import (
    SYMBOL,
    MAGIC_NUMBER,
    DEVIATION
)

from broker_manager import get_filling_mode


def close_position():

    positions = mt5.positions_get(symbol=SYMBOL)

    if positions is None:
        print("❌ No Position Found")
        return None

    if len(positions) == 0:
        print("ℹ️ No Open Position")
        return None

    position = positions[0]

    tick = mt5.symbol_info_tick(SYMBOL)

    if tick is None:
        print("❌ Tick Data Not Available")
        return None

    if position.type == mt5.POSITION_TYPE_BUY:

        order_type = mt5.ORDER_TYPE_SELL
        price = tick.bid

    else:

        order_type = mt5.ORDER_TYPE_BUY
        price = tick.ask

    request = {

        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": SYMBOL,
        "volume": position.volume,
        "type": order_type,
        "position": position.ticket,
        "price": price,
        "deviation": DEVIATION,
        "magic": MAGIC_NUMBER,
        "comment": "AI Bot Close",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": get_filling_mode()

    }

    result = mt5.order_send(request)

    if result is None:
        print("❌ Close Order Failed")
        return None

    if result.retcode == mt5.TRADE_RETCODE_DONE:
        print("✅ Position Closed Successfully")
    else:
        print(f"❌ Close Failed : {result.retcode}")
        print(result.comment)

    return result