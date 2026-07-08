import MetaTrader5 as mt5

from config import (
    SYMBOL,
    MAGIC_NUMBER,
    DEVIATION
)

from live_trading.broker_manager import get_filling_mode
from mt5.retcode_manager import get_retcode_message


def execute_order(order_type, lot, sl, tp):

    tick = mt5.symbol_info_tick(SYMBOL)

    if tick is None:
        print("❌ Tick Data Not Available")
        return None

    # BUY uses Ask Price
    if order_type == mt5.ORDER_TYPE_BUY:
        price = tick.ask
        comment = "AI Bot BUY"

    # SELL uses Bid Price
    else:
        price = tick.bid
        comment = "AI Bot SELL"

    request = {

        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": SYMBOL,
        "volume": lot,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": DEVIATION,
        "magic": MAGIC_NUMBER,
        "comment": comment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": get_filling_mode()

    }

    result = mt5.order_send(request)

    if result is None:
        print("❌ Order Send Failed")
        print(mt5.last_error())
        return None

    if result.retcode == mt5.TRADE_RETCODE_DONE:

        if order_type == mt5.ORDER_TYPE_BUY:
            print("✅ BUY Order Executed")
        else:
            print("✅ SELL Order Executed")

    else:

        print(f"❌ Order Failed : {result.retcode}")
        print(get_retcode_message(result.retcode))

    return result


def buy(lot, sl, tp):

    return execute_order(
        mt5.ORDER_TYPE_BUY,
        lot,
        sl,
        tp
    )


def sell(lot, sl, tp):

    return execute_order(
        mt5.ORDER_TYPE_SELL,
        lot,
        sl,
        tp
    )