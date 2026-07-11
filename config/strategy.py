"""
Strategy Configuration
"""

import MetaTrader5 as mt5

# ==========================================
# EMA SETTINGS
# ==========================================

FAST_EMA = 9
SLOW_EMA = 20

# ==========================================
# ATR SETTINGS
# ==========================================

ATR_PERIOD = 14

ATR_SL_MULTIPLIER = 2.0

ATR_TRAILING_MULTIPLIER = 1.5

# ==========================================
# Pullback Settings
# ==========================================

PULLBACK_ATR_MULTIPLIER = 0.20
PULLBACK_BODY_PERCENT = 0.50

# ==========================================
# Trend Settings
# ==========================================

TREND_LOOKBACK = 3

# ==========================================
# Swing Settings
# ==========================================

SWING_LOOKBACK = 10

# ==========================================
# Risk Reward
# ==========================================

RISK_REWARD = 2.0

# ==========================================
# Confirmation
# ==========================================

USE_CANDLE_CONFIRMATION = True
CONFIRMATION_BODY_PERCENT = 0.60
CONFIRMATION_WICK_PERCENT = 0.20

# ==========================================
# RSI
# ==========================================

RSI_PERIOD = 14

# ==========================================
# ATR
# ==========================================

ATR_PERIOD = 14

# ==========================================
# STOP LOSS
# ==========================================


USE_SWING_STOP = True
USE_BROKER_STOP = True

# ==========================================
# BREAK EVEN
# ==========================================

USE_BREAK_EVEN = True

BREAK_EVEN_R = 1.0

# ==========================================
# TRAILING STOP
# ==========================================

USE_TRAILING_STOP = True

# ==========================================
# CONFLUENCE ENGINE (PHASE 0)
# ==========================================

CONFLUENCE_THRESHOLD = 70      # 0-100 scale for entry decision
TREND_WEIGHT = 1.0             # weight for trend detector
CONFIRMATION_WEIGHT = 1.0      # weight for confirmation detector
BREAKOUT_WEIGHT = 1.0          # weight for breakout detector
PULLBACK_WEIGHT = 1.0          # weight for pullback detector
MARKET_STRUCTURE_WEIGHT = 1.0  # weight for market structure detector
BOS_WEIGHT = 1.5               # weight for BOS detector
CHOCH_WEIGHT = 1.2             # weight for CHOCH detector
COUNTER_TREND_FACTOR = 0.8     # multiplier for signals opposing HTf trend

# ==========================================
# MARKET STRUCTURE / BOS / CHOCH SETTINGS (PHASE 1)
# ==========================================

SWING_LOOKBACK = 10                        # swing lookback period
BOS_CONFIRMATION_CLOSE = True              # True = close-based, False = wick-based
BOS_MIN_BREAK_PIPS = 5                     # minimum break size in pips (0 to disable)
BOS_MIN_BREAK_ATR = 0.5                    # minimum break size in ATR multiples (0 to disable)

# ==========================================
# FVG SETTINGS (PHASE 2)
# ==========================================

FVG_MIN_GAP_PIPS = 5                       # minimum gap size in pips (0 to disable)
FVG_MIN_GAP_ATR = 0.5                      # minimum gap size in ATR multiples (0 to disable)
FVG_EXPIRY_CANDLES = 20                    # number of candles after which an FVG expires
FVG_BODY_FILTER = 0.5                      # middle cation body-to-range ratio (0-1, 0 to disable)
FVG_WEIGHT = 1.0                           # weight for FVG detector in confluence engine
FVG_PULLBACK_TOLERANCE = 0.1               # tolerance for FVG touch in pullback detection (ATR multiples)

# ==========================================
# SUPPORT/RESISTANCE ZONE SETTINGS (PHASE 3)
# ==========================================

SR_ZONE_CLUSTER_ATR = 0.3           # cluster tolerance in ATR multiples (0 to disable)
SR_ZONE_CLUSTER_PIPS = 5            # cluster tolerance in pips (0 to disable)
SR_MAX_TOUCHES_FOR_SCORE = 10       # touch count for max score (normalization)
SR_ZONE_EXPIRY_CANDLES = 50         # max age of zone in candles
SR_WICK_NORMALIZER_ATR = 2.0        # ATR multiplier for wick normalization
SR_MIN_TOUCHES = 2                  # minimum touches for valid zone
SR_VIOLATION_ATR = 0.5              # violation size in ATR multiples (0 to disable)
SR_VIOLATION_PIPS = 3               # violation size in pips (0 to disable)
SR_MAX_ZONE_WIDTH_ATR = 3.0         # max zone width in ATR multiples (0 to disable)
SR_WEIGHT = 1.0                     # weight for SR zone detector in confluence engine

# ==========================================
# FIBONACCI SETTINGS (PHASE 3.5)
# ==========================================

FIBONACCI_WEIGHT = 1.0                     # weight for Fibonacci detector in confluence engine

# ==========================================
# HIGHER TIMEFRAME BIAS SETTINGS
# ==========================================

HTF_TIMEFRAME = mt5.TIMEFRAME_H4       # higher‑timeframe for bias (e.g., H4)
HTF_EMA_PERIOD = 200                   # EMA period for higher‑timeframe bias

# ==========================================
# CHOPPINESS FILTER SETTINGS (ADX)
# ==========================================

ADX_PERIOD = 14
ADX_MIN_THRESHOLD = 20                 # ADX below this indicates choppy/ranging market

# ==========================================
# RISK MANAGEMENT PARAMETERS (PHASE 6)
# ==========================================

RISK_PER_TRADE = 2.0                     # Percent of account to risk per trade (e.g., 2.0 for 2%)
FALLBACK_SL_PIPS = 20                    # Fallback stop loss in pips when ATR is unavailable
MIN_RISK_REWARD = 1.0                    # Minimum acceptable risk-reward ratio

# ==========================================
# Debug
# ==========================================

DEBUG_STRATEGY = True