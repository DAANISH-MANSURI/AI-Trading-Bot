import MetaTrader5 as mt5


def can_open_trade(symbol):

    positions = mt5.positions_get(symbol=symbol)

    if positions is None:
        return True

    if len(positions) == 0:
        return True

    return False