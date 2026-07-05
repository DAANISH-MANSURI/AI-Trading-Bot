from enum import Enum


# ==========================================
# Trade Signals
# ==========================================

class Signal(Enum):

    BUY = "BUY"

    SELL = "SELL"

    NO_TRADE = "NO_TRADE"


# ==========================================
# Trade Result
# ==========================================

class TradeStatus(Enum):

    WIN = "WIN"

    LOSS = "LOSS"


# ==========================================
# Exit Reason
# ==========================================

class ExitReason(Enum):

    TP = "TP"

    SL = "SL"

    MANUAL = "MANUAL"


# ==========================================
# Position Direction
# ==========================================

class PositionType(Enum):

    LONG = "LONG"

    SHORT = "SHORT"


# ==========================================
# Account Status
# ==========================================

class AccountStatus(Enum):

    ACTIVE = "ACTIVE"

    DISABLED = "DISABLED"

    STOPPED = "STOPPED"

# ==========================================
# Market Trend
# ==========================================

class Trend(Enum):

    BULLISH = "BULLISH"

    BEARISH = "BEARISH"

    SIDEWAYS = "SIDEWAYS"