from enum import Enum


# ==========================================
# Trade Signals
# ==========================================

class Signal(Enum):
    """
    Trading Signals
    """

    # Entry
    BUY = "BUY"
    SELL = "SELL"

    # Waiting For Breakout Confirmation
    WAIT_BUY = "WAIT_BUY"
    WAIT_SELL = "WAIT_SELL"

    # Exit Signals
    EXIT_BUY = "EXIT_BUY"
    EXIT_SELL = "EXIT_SELL"

    # No Trade
    NO_TRADE = "NO_TRADE"


# ==========================================
# Trade Status
# ==========================================

class TradeStatus(Enum):
    """
    Trade Result
    """

    OPEN = "OPEN"
    CLOSED = "CLOSED"

    WIN = "WIN"
    LOSS = "LOSS"


# ==========================================
# Exit Reason
# ==========================================

class ExitReason(Enum):
    """
    Why trade was closed
    """

    TP = "TP"
    SL = "SL"

    TRAILING = "TRAILING"
    BREAKEVEN = "BREAKEVEN"
    EMA_EXIT = "EMA_EXIT"

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