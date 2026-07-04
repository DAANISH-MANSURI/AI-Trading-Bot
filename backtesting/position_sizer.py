import MetaTrader5 as mt5


def calculate_position_size(
    symbol,
    balance,
    risk_percent,
    entry_price,
    stop_loss
):
    """
    Calculate lot size based on account balance and risk.
    """

    symbol_info = mt5.symbol_info(symbol)

    if symbol_info is None:
        return 0.01

    tick_value = symbol_info.trade_tick_value
    point = symbol_info.point

    sl_distance = abs(entry_price - stop_loss)

    if sl_distance <= 0:
        return symbol_info.volume_min

    risk_amount = balance * (risk_percent / 100)

    risk_per_lot = (sl_distance / point) * tick_value

    if risk_per_lot <= 0:
        return symbol_info.volume_min

    lot = risk_amount / risk_per_lot

    # Broker Limits
    lot = max(symbol_info.volume_min, lot)
    lot = min(symbol_info.volume_max, lot)

    # Round to Broker Step
    step = symbol_info.volume_step

    lot = round(lot / step) * step

    return round(lot, 2)