"""
Risk Management Engine

Calculates stop loss, take profit, and lot size based on market structure and account risk.
"""

import pandas as pd
from strategy.shared.market_structure import get_swing_lows, get_swing_highs
from strategy.shared.sr_zones import get_sr_signal
from risk.lot_size import round_lot, calculate_lot
from config.strategy import MIN_RISK_REWARD


def calculate_risk(balance, risk_percent):
    """
    Original function: calculates risk amount from balance and risk percent.
    Kept for backward compatibility.
    """
    return balance * (risk_percent / 100)


def calculate_trade_levels(symbol, df, signal, account_balance, risk_percent, rr_ratio=2.0, atr_multiplier=1.5):
    """
    Calculate stop loss, take profit, and lot size for a trade based on market structure.

    Parameters:
        symbol (str): Trading symbol (e.g., "EURUSD")
        df (DataFrame): OHLCV data with 'ATR' column
        signal (str): 'BUY' or 'SELL'
        account_balance (float): Account balance in currency
        risk_percent (float): Percent of balance to risk (e.g., 1.0 for 1%)
        rr_ratio (float): Risk-reward ratio for take profit (default 2.0)
        atr_multiplier (float): Multiple for ATR-based stop (default 1.5)

    Returns:
        tuple: (stop_loss, take_profit, lot_size) or (None, None, None) if calculation fails
    """
    try:
        # Calculate risk amount
        risk_amount = account_balance * (risk_percent / 100)

        # Get latest candle data
        if len(df) == 0:
            return None, None, None

        last_close = float(df.iloc[-1]['close'])
        atr = float(df.iloc[-1]['ATR']) if 'ATR' in df.columns and not pd.isna(df.iloc[-1]['ATR']) else 0.0

        # Get swing points
        swing_lows = get_swing_lows(df)
        swing_highs = get_swing_highs(df)

        # Determine stop loss based on signal
        if signal == 'BUY':
            # For buy, stop loss below entry
            if not swing_lows or len(swing_lows) == 0:
                # No swing lows found, use ATR-based stop
                sl_price = last_close - (atr * atr_multiplier)
            else:
                # Most recent swing low
                recent_swing_low = float(swing_lows[-1]['price'])
                # Ensure stop is at least ATR*multiplier away
                min_sl_distance = atr * atr_multiplier
                actual_sl_distance = last_close - recent_swing_low
                if actual_sl_distance < min_sl_distance:
                    # Use ATR-based stop if structure is too close
                    sl_price = last_close - min_sl_distance
                else:
                    # Use structure-based stop
                    sl_price = recent_swing_low

            # Ensure stop loss is below entry
            if sl_price >= last_close:
                sl_price = last_close - (atr * atr_multiplier)

        elif signal == 'SELL':
            # For sell, stop loss above entry
            if not swing_highs or len(swing_highs) == 0:
                # No swing highs found, use ATR-based stop
                sl_price = last_close + (atr * atr_multiplier)
            else:
                # Most recent swing high
                recent_swing_high = float(swing_highs[-1]['price'])
                # Ensure stop is at least ATR*multiplier away
                min_sl_distance = atr * atr_multiplier
                actual_sl_distance = recent_swing_high - last_close
                if actual_sl_distance < min_sl_distance:
                    # Use ATR-based stop if structure is too close
                    sl_price = last_close + min_sl_distance
                else:
                    # Use structure-based stop
                    sl_price = recent_swing_high

            # Ensure stop loss is above entry
            if sl_price <= last_close:
                sl_price = last_close + (atr * atr_multiplier)
        else:
            # Invalid signal
            return None, None, None

        # Calculate take profit: try S/R zone first, then fixed RR
        tp_price = None
        risk_per_share = abs(last_close - sl_price)
        if risk_per_share > 0:
            if signal in ('BUY', 'SELL'):
                sr_signal = get_sr_signal(df)
                # sr_signal.direction is the trade direction suggested by the SR signal (BUY for support bounce, SELL for resistance reject)
                # For our trade, we want the opposite: if we are BUY, we look for SELL SR signal (resistance)
                # If we are SELL, we look for BUY SR signal (support)
                if sr_signal.direction == ('SELL' if signal == 'BUY' else 'BUY') and sr_signal.score > 0:
                    zone_low = float(sr_signal.meta.get('zone_low', 0.0))
                    zone_high = float(sr_signal.meta.get('zone_high', 0.0))
                    if signal == 'BUY':
                        # Target bottom of resistance zone
                        candidate_tp = zone_low
                        # Ensure candidate is above entry and meaningful
                        if candidate_tp > last_close:
                            candidate_rr = abs(candidate_tp - last_close) / risk_per_share
                            if candidate_rr >= MIN_RISK_REWARD:
                                tp_price = candidate_tp
                    else:  # SELL
                        # Target top of support zone
                        candidate_tp = zone_high
                        # Ensure candidate is below entry and meaningful
                        if candidate_tp < last_close:
                            candidate_rr = abs(candidate_tp - last_close) / risk_per_share
                            if candidate_rr >= MIN_RISK_REWARD:
                                tp_price = candidate_tp
        # If we didn't get a valid SR TP, fall back to fixed RR
        if tp_price is None:
            if signal == 'BUY':
                tp_price = last_close + (risk_per_share * rr_ratio)
            else:  # SELL
                tp_price = last_close - (risk_per_share * rr_ratio)

        # Calculate lot size using the lot_size module
        lot_size = calculate_lot(symbol, risk_amount, last_close, sl_price)

        # Ensure lot size is valid
        if lot_size <= 0:
            lot_size = 0.01  # Fallback to minimum lot size, should be replaced by get_min_lot() but we don't have symbol context here easily

        return sl_price, tp_price, lot_size

    except Exception as e:
        # In case of any error, return None values
        return None, None, None