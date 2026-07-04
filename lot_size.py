import MetaTrader5 as mt5


def calculate_lot(symbol, risk_amount, entry_price, stop_loss):

    symbol_info = mt5.symbol_info(symbol)

    if symbol_info is None:
        return 0.01

    tick_value = symbol_info.trade_tick_value
    point = symbol_info.point

    sl_distance = abs(entry_price - stop_loss)

    if sl_distance == 0:
        return symbol_info.volume_min

    risk_per_lot = (sl_distance / point) * tick_value

    lot = risk_amount / risk_per_lot

    # Broker limits
    lot = max(symbol_info.volume_min, lot)
    lot = min(symbol_info.volume_max, lot)

    # Round to broker step
    step = symbol_info.volume_step
    lot = round(lot / step) * step

    return round(lot, 2)