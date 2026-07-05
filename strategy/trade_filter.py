from candle_patterns import (
    bullish_engulfing,
    bearish_engulfing,
    pin_bar
)


# ==========================================
# BUY FILTER
# ==========================================

def allow_buy(df):

    last = df.iloc[-1]

    ema_ok = (

        last["EMA5"] >
        last["EMA9"] >
        last["EMA13"] >
        last["EMA21"] >
        last["EMA200"]

    )

    rsi_ok = last["RSI"] > 55

    # --------------------------------------
    # TESTING MODE
    # Candle Pattern Disabled
    # --------------------------------------

    return ema_ok and rsi_ok


# ==========================================
# SELL FILTER
# ==========================================

def allow_sell(df):

    last = df.iloc[-1]

    ema_ok = (

        last["EMA5"] <
        last["EMA9"] <
        last["EMA13"] <
        last["EMA21"] <
        last["EMA200"]

    )

    rsi_ok = last["RSI"] < 45

    # --------------------------------------
    # TESTING MODE
    # Candle Pattern Disabled
    # --------------------------------------

    return ema_ok and rsi_ok