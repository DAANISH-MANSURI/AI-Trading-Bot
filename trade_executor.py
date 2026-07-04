import MetaTrader5 as mt5

from config import (
    SYMBOL,
    LOT_SIZE,
    MAGIC_NUMBER,
    DEVIATION
)


def buy(sl=None, tp=None):

    symbol_info = mt5.symbol_info(SYMBOL)

    if symbol_info is None:
        print("❌ Symbol Not Found")
        return None

    if not symbol_info.visible:
        mt5.symbol_select(SYMBOL, True)

    tick = mt5.symbol_info_tick(SYMBOL)

    if tick is None:
        print("❌ No Tick Data")
        return None

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": SYMBOL,
        "volume": LOT_SIZE,
        "type": mt5.ORDER_TYPE_BUY,
        "price": tick.ask,
        "sl": sl if sl else 0.0,
        "tp": tp if tp else 0.0,
        "deviation": DEVIATION,
        "magic": MAGIC_NUMBER,
        "comment": "AI Bot BUY",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK
    }

    result = mt5.order_send(request)

    return result


def sell(sl=None, tp=None):

    symbol_info = mt5.symbol_info(SYMBOL)

    if symbol_info is None:
        print("❌ Symbol Not Found")
        return None

    if not symbol_info.visible:
        mt5.symbol_select(SYMBOL, True)

    tick = mt5.symbol_info_tick(SYMBOL)

    if tick is None:
        print("❌ No Tick Data")
        return None

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": SYMBOL,
        "volume": LOT_SIZE,
        "type": mt5.ORDER_TYPE_SELL,
        "price": tick.bid,
        "sl": sl if sl else 0.0,
        "tp": tp if tp else 0.0,
        "deviation": DEVIATION,
        "magic": MAGIC_NUMBER,
        "comment": "AI Bot SELL",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK
    }

    result = mt5.order_send(request)

    return result