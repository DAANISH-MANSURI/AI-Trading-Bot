import MetaTrader5 as mt5
import pandas as pd


def get_historical_data(
    symbol,
    timeframe,
    candles=5000
):

    rates = mt5.copy_rates_from_pos(
        symbol,
        timeframe,
        0,
        candles
    )

    if rates is None:
        return None

    df = pd.DataFrame(rates)

    df["time"] = pd.to_datetime(
        df["time"],
        unit="s"
    )

    return df