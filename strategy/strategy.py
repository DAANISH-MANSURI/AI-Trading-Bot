from core.enums import Signal, Trend
from core.constants import (
    RSI_BUY_LEVEL,
    RSI_SELL_LEVEL
)

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

        if close > ema5 and rsi > RSI_BUY_LEVEL:
            return {
                "trend": "BULLISH",
                "signal": Signal.BUY,
                "reason": "Price above EMA5 in bullish trend"
            }

        else:
            return {
                "trend": Trend.BULLISH,
                "signal": Signal.NO_TRADE,
                "reason": "Waiting for pullback"
            }

    # Bearish Trend
    elif ema5 < ema9 < ema13 < ema21 < ema200:

        if close < ema5 and rsi < RSI_SELL_LEVEL:
            return {
                "trend": Trend.BEARISH,
                "signal": Signal.SELL,
                "reason": "Price below EMA5 in bearish trend"
            }

        else:
            return {
                "trend": Trend.BEARISH,
                "signal": Signal.NO_TRADE,
                "reason": "Waiting for pullback"
            }

    return {
        "trend": Trend.SIDEWAYS,
        "signal": Signal.NO_TRADE,
        "reason": "Market is ranging"
    }