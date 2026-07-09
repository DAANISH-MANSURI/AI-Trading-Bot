"""
Trade Filter

Combined filter for market structure, FVG, S/R, session, and spread.
"""

from strategy.shared.market_structure import bullish_structure, bearish_structure
from strategy.shared.fvg import get_fvg_signal
from strategy.shared.sr_zones import get_sr_signal
from strategy.session_filter import trading_session
from strategy.spread_filter import spread_ok


def allow_buy(df):
    # Check market structure is bullish
    if not bullish_structure(df):
        return False

    # Check FVG: bullish FVG present and price near (signal generated)
    fvg_signal = get_fvg_signal(df)
    if fvg_signal.direction != "BUY" or fvg_signal.score == 0:
        return False

    # Check S/R: support zone present and price near (signal generated as BUY)
    sr_signal = get_sr_signal(df)
    if sr_signal.direction != "BUY" or sr_signal.score == 0:
        return False

    # Check session
    if not trading_session():
        return False

    # Check spread
    if not spread_ok():
        return False

    return True


def allow_sell(df):
    # Check market structure is bearish
    if not bearish_structure(df):
        return False

    # Check FVG: bearish FVG present and price near (signal generated)
    fvg_signal = get_fvg_signal(df)
    if fvg_signal.direction != "SELL" or fvg_signal.score == 0:
        return False

    # Check S/R: resistance zone present and price near (signal generated as SELL)
    sr_signal = get_sr_signal(df)
    if sr_signal.direction != "SELL" or sr_signal.score == 0:
        return False

    # Check session
    if not trading_session():
        return False

    # Check spread
    if not spread_ok():
        return False

    return True