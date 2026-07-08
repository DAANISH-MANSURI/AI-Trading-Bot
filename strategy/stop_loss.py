"""
EMA Crossover Stop Loss Engine
"""

from core.enums import Signal

from mt5.symbol_info import (
    get_stop_level,
    get_point,
    get_digits
)

ATR_MULTIPLIER = 1.5
LOOKBACK = 10
RR = 2.0


# ==========================================
# SIMPLE SWINGS
# ==========================================

def recent_swing_low(df):

    return df["low"].tail(LOOKBACK).min()


def recent_swing_high(df):

    return df["high"].tail(LOOKBACK).max()


# ==========================================
# ATR STOP
# ==========================================

def atr_distance(df):

    atr = df.iloc[-1]["ATR"]

    broker = get_stop_level() * get_point()

    return max(

        atr * ATR_MULTIPLIER,

        broker

    )


# ==========================================
# BUY
# ==========================================

def buy_stop_loss(df):

    entry = df.iloc[-1]["close"]

    swing = recent_swing_low(df)

    atr_sl = entry - atr_distance(df)

    return min(

        swing,

        atr_sl

    )


# ==========================================
# SELL
# ==========================================

def sell_stop_loss(df):

    entry = df.iloc[-1]["close"]

    swing = recent_swing_high(df)

    atr_sl = entry + atr_distance(df)

    return max(

        swing,

        atr_sl

    )


# ==========================================
# MAIN
# ==========================================

def calculate_sl_tp(df, signal):

    entry = df.iloc[-1]["close"]

    if signal == Signal.BUY:

        sl = buy_stop_loss(df)

        risk = entry - sl

        tp = entry + (risk * RR)

    elif signal == Signal.SELL:

        sl = sell_stop_loss(df)

        risk = sl - entry

        tp = entry - (risk * RR)

    else:

        return None, None

    return (

        round(sl, get_digits()),

        round(tp, get_digits())

    )