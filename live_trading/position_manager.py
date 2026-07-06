import MetaTrader5 as mt5
from config import SYMBOL


def has_open_position(symbol=SYMBOL):

    positions = mt5.positions_get(symbol=symbol)

    if positions is None:
        return False

    return len(positions) > 0


def get_position():

    positions = mt5.positions_get(symbol=SYMBOL)

    if positions is None:
        return None

    if len(positions) == 0:
        return None

    return positions[0]


def get_position_type():

    position = get_position()

    if position is None:
        return None

    if position.type == mt5.POSITION_TYPE_BUY:
        return "BUY"

    elif position.type == mt5.POSITION_TYPE_SELL:
        return "SELL"

    return None


def get_position_ticket():

    position = get_position()

    if position is None:
        return None

    return position.ticket


def get_position_volume():

    position = get_position()

    if position is None:
        return 0.0

    return position.volume


def get_position_profit():

    position = get_position()

    if position is None:
        return 0.0

    return position.profit


def get_open_price():

    position = get_position()

    if position is None:
        return None

    return position.price_open


def get_stop_loss():

    position = get_position()

    if position is None:
        return None

    return position.sl


def get_take_profit():

    position = get_position()

    if position is None:
        return None

    return position.tp

def wait_until_position_closed(timeout=10):

    import time

    start = time.time()

    while True:

        positions = mt5.positions_get(symbol=SYMBOL)

        if positions is None:
            return False

        if len(positions) == 0:
            return True

        if time.time() - start > timeout:
            return False

        time.sleep(0.5)

# ==========================================
# Position Information
# ==========================================

def get_entry_price():

    return get_open_price()


def get_position_sl_tp():

    position = get_position()

    if position is None:

        return None, None

    return (

        position.sl,

        position.tp

    )