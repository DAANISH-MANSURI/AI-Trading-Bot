import MetaTrader5 as mt5

from config import (
    SYMBOL,
    MAGIC_NUMBER,
    DEVIATION,
    FILLING_MODE
)


def buy(lot, sl, tp):

    tick = mt5.symbol_info_tick(SYMBOL)

    if tick is None:
        print("❌ Tick Data Not Available")
        return None

    request = {

        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": SYMBOL,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": tick.ask,
        "sl": sl,
        "tp": tp,
        "deviation": DEVIATION,
        "magic": MAGIC_NUMBER,
        "comment": "AI Bot BUY",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": FILLING_MODE

    }

    result = mt5.order_send(request)

    if result is None:
        print("❌ BUY Order Failed")
        return None

    if result.retcode == mt5.TRADE_RETCODE_DONE:
        print("✅ BUY Order Executed")
    else:
        print(f"❌ BUY Failed : {result.retcode}")
        print(result.comment)

    return result


def sell(lot, sl, tp):

    tick = mt5.symbol_info_tick(SYMBOL)

    if tick is None:
        print("❌ Tick Data Not Available")
        return None

    request = {

        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": SYMBOL,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "price": tick.bid,
        "sl": sl,
        "tp": tp,
        "deviation": DEVIATION,
        "magic": MAGIC_NUMBER,
        "comment": "AI Bot SELL",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": FILLING_MODE

    }

    result = mt5.order_send(request)

    if result is None:
        print("❌ SELL Order Failed")
        return None

    if result.retcode == mt5.TRADE_RETCODE_DONE:
        print("✅ SELL Order Executed")
    else:
        print(f"❌ SELL Failed : {result.retcode}")
        print(result.comment)

    return result