last_candle_time = None


def is_new_candle(df):
    global last_candle_time

    current_time = df.iloc[-1]["time"]

    if last_candle_time is None:
        last_candle_time = current_time
        return True

    if current_time != last_candle_time:
        last_candle_time = current_time
        return True

    return False