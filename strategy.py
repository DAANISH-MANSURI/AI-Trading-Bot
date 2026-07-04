def get_signal(df):

    last = df.iloc[-1]
    rsi = last["RSI"]
    ema5 = last["EMA5"]
    ema9 = last["EMA9"]
    ema13 = last["EMA13"]
    ema21 = last["EMA21"]
    ema200 = last["EMA200"]
    close = last["close"]

    # Bullish Trend
    if ema5 > ema9 > ema13 > ema21 > ema200:

        if close > ema5 and rsi > 55:
            return {
                "trend": "BULLISH",
                "signal": "BUY",
                "reason": "Price above EMA5 in bullish trend"
            }

        else:
            return {
                "trend": "BULLISH",
                "signal": "NO_TRADE",
                "reason": "Waiting for pullback"
            }

    # Bearish Trend
    elif ema5 < ema9 < ema13 < ema21 < ema200:

        if close < ema5 and rsi < 45:
            return {
                "trend": "BEARISH",
                "signal": "SELL",
                "reason": "Price below EMA5 in bearish trend"
            }

        else:
            return {
                "trend": "BEARISH",
                "signal": "NO_TRADE",
                "reason": "Waiting for pullback"
            }

    return {
        "trend": "SIDEWAYS",
        "signal": "NO_TRADE",
        "reason": "Market is ranging"
    }