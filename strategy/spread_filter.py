import MetaTrader5 as mt5

from config import SYMBOL, MAX_SPREAD

from mt5.symbol_info import (
    get_symbol_info,
    get_point
)


def spread_ok():

    tick = mt5.symbol_info_tick(SYMBOL)

    if tick is None:
        return False

    point = get_point()

    spread = (tick.ask - tick.bid) / point

    return spread <= MAX_SPREAD


def get_spread():

    tick = mt5.symbol_info_tick(SYMBOL)

    if tick is None:
        return 0

    point = get_point()

    spread = (tick.ask - tick.bid) / point

    return round(spread, 1)