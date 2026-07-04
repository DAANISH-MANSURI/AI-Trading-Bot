def simulate_trade(df, entry_index, signal, sl, tp):

    entry_candle = df.iloc[entry_index]

    entry_time = entry_candle["time"]
    entry_price = entry_candle["close"]

    # Risk & Reward
    risk_points = abs(entry_price - sl)
    reward_points = abs(tp - entry_price)

    for i in range(entry_index + 1, len(df)):

        candle = df.iloc[i]

        exit_time = candle["time"]

        high = candle["high"]
        low = candle["low"]

        duration = i - entry_index

        # =====================================
        # BUY
        # =====================================

        if signal == "BUY":

            # Stop Loss Hit
            if low <= sl:

                profit_points = sl - entry_price

                return {

                    "result": "LOSS",

                    "signal": signal,

                    "entry_time": entry_time,
                    "exit_time": exit_time,

                    "entry_price": round(entry_price, 2),
                    "exit_price": round(sl, 2),

                    "risk_points": round(risk_points, 2),
                    "reward_points": round(reward_points, 2),
                    "profit_points": round(profit_points, 2),

                    "rr": round(
                        reward_points / risk_points,
                        2
                    ),

                    "trade_duration": duration,

                    "exit_reason": "SL",

                    "exit_index": i

                }

            # Take Profit Hit
            if high >= tp:

                profit_points = tp - entry_price

                return {

                    "result": "WIN",

                    "signal": signal,

                    "entry_time": entry_time,
                    "exit_time": exit_time,

                    "entry_price": round(entry_price, 2),
                    "exit_price": round(tp, 2),

                    "risk_points": round(risk_points, 2),
                    "reward_points": round(reward_points, 2),
                    "profit_points": round(profit_points, 2),

                    "rr": round(
                        reward_points / risk_points,
                        2
                    ),

                    "trade_duration": duration,

                    "exit_reason": "TP",

                    "exit_index": i

                }

        # =====================================
        # SELL
        # =====================================

        elif signal == "SELL":

            # Stop Loss Hit
            if high >= sl:

                profit_points = entry_price - sl

                return {

                    "result": "LOSS",

                    "signal": signal,

                    "entry_time": entry_time,
                    "exit_time": exit_time,

                    "entry_price": round(entry_price, 2),
                    "exit_price": round(sl, 2),

                    "risk_points": round(risk_points, 2),
                    "reward_points": round(reward_points, 2),
                    "profit_points": round(profit_points, 2),

                    "rr": round(
                        reward_points / risk_points,
                        2
                    ),

                    "trade_duration": duration,

                    "exit_reason": "SL",

                    "exit_index": i

                }

            # Take Profit Hit
            if low <= tp:

                profit_points = entry_price - tp

                return {

                    "result": "WIN",

                    "signal": signal,

                    "entry_time": entry_time,
                    "exit_time": exit_time,

                    "entry_price": round(entry_price, 2),
                    "exit_price": round(tp, 2),

                    "risk_points": round(risk_points, 2),
                    "reward_points": round(reward_points, 2),
                    "profit_points": round(profit_points, 2),

                    "rr": round(
                        reward_points / risk_points,
                        2
                    ),

                    "trade_duration": duration,

                    "exit_reason": "TP",

                    "exit_index": i

                }

    return None