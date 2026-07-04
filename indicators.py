from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange


def add_indicators(df):

    # EMA
    df["EMA5"] = EMAIndicator(df["close"], window=5).ema_indicator()
    df["EMA9"] = EMAIndicator(df["close"], window=9).ema_indicator()
    df["EMA13"] = EMAIndicator(df["close"], window=13).ema_indicator()
    df["EMA21"] = EMAIndicator(df["close"], window=21).ema_indicator()
    df["EMA200"] = EMAIndicator(df["close"], window=200).ema_indicator()

    # RSI
    df["RSI"] = RSIIndicator(df["close"], window=14).rsi()

    # ATR
    atr = AverageTrueRange(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        window=14
    )

    df["ATR"] = atr.average_true_range()

    return df