import MetaTrader5 as mt5

# ===========================
# Trading Settings
# ===========================

SYMBOL = "BTCUSD"
TIMEFRAME = mt5.TIMEFRAME_M5
BARS = 250

# ===========================
# Risk Management
# ===========================

RISK_PERCENT = 1          # Risk per Trade (%)
LOT_SIZE = 0.01

# ===========================
# Trade Settings
# ===========================

MAGIC_NUMBER = 123456
DEVIATION = 20

# ===========================
# Spread Filter
# ===========================

# BTCUSD ke liye testing value
MAX_SPREAD = 5000

# ===========================
# Break Even Settings
# ===========================

# Trigger in POINTS
BREAK_EVEN_TRIGGER = 100

# ===========================
# Trailing Stop Settings
# ===========================

TRAILING_ATR_MULTIPLIER = 1.5
TRAILING_START_ATR = 1.0

# ===========================
# Auto Trading
# ===========================

AUTO_TRADING = True