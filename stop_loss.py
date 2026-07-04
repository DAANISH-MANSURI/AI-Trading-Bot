def calculate_sl_tp(df, signal):

    last = df.iloc[-1]

    atr = last["ATR"]

    if signal == "BUY":

        sl = last["close"] - (atr * 2)

        tp = last["close"] + (atr * 4)

    elif signal == "SELL":

        sl = last["close"] + (atr * 2)

        tp = last["close"] - (atr * 4)

    else:

        return None, None

    return round(sl, 2), round(tp, 2)