from config import MAX_SPREAD

from mt5.symbol_info import get_spread as get_mt5_spread


def spread_ok():

    spread = get_mt5_spread()

    return spread <= MAX_SPREAD


def get_spread():

    return round(get_mt5_spread(), 1)