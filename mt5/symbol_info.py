import MetaTrader5 as mt5

from config.mt5 import SYMBOL


def get_symbol_info():

    symbol = mt5.symbol_info(SYMBOL)

    if symbol is None:

        raise Exception(f"{SYMBOL} not found")

    return symbol


# ==========================================
# Price Information
# ==========================================

def get_point():

    return get_symbol_info().point


def get_digits():

    return get_symbol_info().digits


# ==========================================
# Broker Rules
# ==========================================

def get_stop_level():

    return get_symbol_info().trade_stops_level


def get_freeze_level():

    return get_symbol_info().trade_freeze_level


# ==========================================
# Volume
# ==========================================

def get_min_lot():

    return get_symbol_info().volume_min


def get_max_lot():

    return get_symbol_info().volume_max


def get_lot_step():

    return get_symbol_info().volume_step


# ==========================================
# Tick
# ==========================================

def get_tick_value():

    return get_symbol_info().trade_tick_value


def get_tick_size():

    return get_symbol_info().trade_tick_size


# ==========================================
# Execution
# ==========================================

def get_execution_mode():

    return get_symbol_info().trade_exemode


def get_filling_mode():

    return mt5.ORDER_FILLING_FOK


# ==========================================
# Spread
# ==========================================

def get_spread():

    return get_symbol_info().spread