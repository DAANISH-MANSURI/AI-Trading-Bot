import MetaTrader5 as mt5


def has_open_position(symbol):

    positions = mt5.positions_get(symbol=symbol)

    if positions is None:
        return False

    return len(positions) > 0