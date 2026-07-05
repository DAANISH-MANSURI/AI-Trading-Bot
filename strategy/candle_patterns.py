def bullish_engulfing(df):

    prev = df.iloc[-2]
    curr = df.iloc[-1]

    return (
        prev["close"] < prev["open"] and
        curr["close"] > curr["open"] and
        curr["open"] < prev["close"] and
        curr["close"] > prev["open"]
    )
def bearish_engulfing(df):

    prev = df.iloc[-2]
    curr = df.iloc[-1]

    return (
        prev["close"] > prev["open"] and
        curr["close"] < curr["open"] and
        curr["open"] > prev["close"] and
        curr["close"] < prev["open"]
    )
def doji(df):

    candle = df.iloc[-1]

    body = abs(candle["close"] - candle["open"])
    total = candle["high"] - candle["low"]

    return body <= total * 0.10
def pin_bar(df):

    candle = df.iloc[-1]

    body = abs(candle["close"] - candle["open"])

    upper = candle["high"] - max(candle["open"], candle["close"])

    lower = min(candle["open"], candle["close"]) - candle["low"]

    return upper > body * 2 or lower > body * 2
