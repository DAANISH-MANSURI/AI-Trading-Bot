"""
Professional Lot Size Engine

Version : 2.0
"""

from mt5.symbol_info import (
    get_symbol_info,
    get_tick_value,
    get_point,
    get_min_lot,
    get_max_lot,
    get_lot_step
)


# ==========================================
# ROUND LOT TO BROKER STEP
# ==========================================

def round_lot(lot):

    step = get_lot_step()

    if step <= 0:
        return round(lot, 2)

    lot = round(lot / step) * step

    return round(lot, 2)


# ==========================================
# CALCULATE LOT SIZE
# ==========================================

def calculate_lot(
    symbol,
    risk_amount,
    entry_price,
    stop_loss
):

    info = get_symbol_info()

    if info is None:
        return get_min_lot()

    point = get_point()
    tick_value = get_tick_value()

    # Stop Loss Distance
    sl_distance = abs(entry_price - stop_loss)

    if sl_distance <= 0:
        return get_min_lot()

    # Distance in Points
    sl_points = sl_distance / point

    if sl_points <= 0:
        return get_min_lot()

    # Risk for 1 Lot
    risk_per_lot = sl_points * tick_value

    if risk_per_lot <= 0:
        return get_min_lot()

    # Raw Lot
    lot = risk_amount / risk_per_lot

    # Broker Limits
    lot = max(lot, get_min_lot())
    lot = min(lot, get_max_lot())

    # Broker Step
    lot = round_lot(lot)

    return lot