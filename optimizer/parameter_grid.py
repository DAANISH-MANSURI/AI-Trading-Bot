from itertools import product

# ==========================================
# EMA Parameters
# ==========================================

EMA_FAST = [5, 7, 9, 10, 12]

EMA_SLOW = [20, 21, 30, 50]

# ==========================================
# RSI Parameters
# ==========================================

RSI_BUY = [55, 58, 60]

RSI_SELL = [45, 42, 40]

# ==========================================
# ATR Parameters
# ==========================================

ATR_SL = [1.5, 2.0]

ATR_TP = [2.0, 2.5, 3.0]

# ==========================================
# Generate All Combinations
# ==========================================

def generate_parameter_grid():

    combinations = product(

        EMA_FAST,

        EMA_SLOW,

        RSI_BUY,

        RSI_SELL,

        ATR_SL,

        ATR_TP

    )

    parameters = []

    for combo in combinations:

        parameters.append({

            "ema_fast": combo[0],

            "ema_slow": combo[1],

            "rsi_buy": combo[2],

            "rsi_sell": combo[3],

            "atr_sl": combo[4],

            "atr_tp": combo[5]

        })

    return parameters