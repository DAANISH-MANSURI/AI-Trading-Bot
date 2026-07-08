"""
Trade Filter

EMA20 Pullback Strategy
"""


# ==========================================
# BUY FILTER
# ==========================================

def allow_buy(df):

    last = df.iloc[-1]

    return last["RSI"] > 50


# ==========================================
# SELL FILTER
# ==========================================

def allow_sell(df):

    last = df.iloc[-1]

    return last["RSI"] < 50