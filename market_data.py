import MetaTrader5 as mt5
import pandas as pd

from config import SYMBOL, TIMEFRAME, BARS


def get_market_data():

    rates = mt5.copy_rates_from_pos(
        SYMBOL,
        TIMEFRAME,
        0,
        BARS
    )

    if rates is None:
        return None

    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")

    return df