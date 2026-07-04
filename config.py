import MetaTrader5 as mt5

# ===========================
# Trading Settings
# ===========================

SYMBOL = "EURUSD"
TIMEFRAME = mt5.TIMEFRAME_M5
BARS = 250

# ===========================
# Risk Management
# ===========================

RISK_PERCENT = 1
LOT_SIZE = 0.01

# ===========================
# Trade Settings
# ===========================

MAGIC_NUMBER = 123456
DEVIATION = 20
# Spread Filter
MAX_SPREAD = 30
#Break Even Settings
BREAK_EVEN_TRIGGER = 0.0010
