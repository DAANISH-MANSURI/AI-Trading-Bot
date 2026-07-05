from broker_manager import (
    get_symbol_info,
    get_min_lot,
    get_max_lot,
    get_lot_step,
    get_tick_value,
    get_point
)


def calculate_lot(symbol, risk_amount, entry_price, stop_loss):

    symbol_info = get_symbol_info()

    if symbol_info is None:
        return 0.01

    tick_value = get_tick_value()
    point = get_point()

    sl_distance = abs(entry_price - stop_loss)

    if sl_distance <= 0:
        return get_min_lot()

    risk_per_lot = (sl_distance / point) * tick_value

    if risk_per_lot <= 0:
        return get_min_lot()

    lot = risk_amount / risk_per_lot

    # Broker Limits
    lot = max(get_min_lot(), lot)
    lot = min(get_max_lot(), lot)

    # Broker Lot Step
    step = get_lot_step()
    lot = round(lot / step) * step

    return round(lot, 2)