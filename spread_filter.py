import MetaTrader5 as mt5
from config import SYMBOL, MAX_SPREAD

def spread_ok():

    tick = mt5.symbol_info_tick(SYMBOL)

    if tick is None:
        return False

    symbol = mt5.symbol_info(SYMBOL)

    if symbol is None:
        return False

    spread = (tick.ask - tick.bid) / symbol.point

    return spread <= MAX_SPREAD


def get_spread():

    tick = mt5.symbol_info_tick(SYMBOL)

    symbol = mt5.symbol_info(SYMBOL)

    if tick is None or symbol is None:
        return 0

    spread = (tick.ask - tick.bid) / symbol.point

    return round(spread, 1)