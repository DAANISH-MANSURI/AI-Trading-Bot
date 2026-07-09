"""
Strategy Router
"""

from strategy.shared.signal import Signal
from strategy.strategies.ema20_pullback import get_signal as ema20_signal
from strategy.strategies.ema_9_20 import get_signal as ema9_signal
from strategy.strategies.ema_crossover import get_signal as ema_crossover_signal
#from strategy.strategies.smart_money import get_signal as smart_money_signal
from strategy.shared.market_structure import (
    get_market_structure_signal,
    get_bos_signal,
    get_choch_signal,
)
from strategy.shared.fvg import get_fvg_signal
from strategy.shared.sr_zones import get_sr_signal
from strategy.shared.fibonacci import get_fibonacci_signal
from strategy.session_filter import trading_session
from strategy.spread_filter import spread_ok
from config.strategy import (
    CONFLUENCE_THRESHOLD,
    COUNTER_TREND_FACTOR,
    TREND_WEIGHT,
    CONFIRMATION_WEIGHT,
    BREAKOUT_WEIGHT,
    PULLBACK_WEIGHT,
    MARKET_STRUCTURE_WEIGHT,
    BOS_WEIGHT,
    CHOCH_WEIGHT,
    FVG_WEIGHT,
    SR_WEIGHT,
    FIBONACCI_WEIGHT,
)
from core.enums import Signal as SignalEnum

__all__ = [
    "get_signal"
]


def get_signal(df):
    """
    Confluence Engine entry point.
    Routes to all available internal and registered detectors, aggregates scores,
    and makes final trading decision.

    Args:
        df: DataFrame containing price data

    Returns: dict with keys matching legacy format for compatibility
    """
    # === SESSION AND SPREAD FILTERS ===
    if not trading_session() or not spread_ok():
        reason = "No trade: outside trading session or spread too wide"
        return {
            "strategy": "Confluence Engine",
            "trend": "NEUTRAL",
            "signal": SignalEnum.NO_TRADE,
            "confidence": 0,
            "reason": reason,
            "setup_high": None,
            "setup_low": None,
            "entry_price": None,
        }

    # ==========================================
    # DETECTOR REGISTRY WITH WEIGHTS FROM CONFIG
    # ==========================================
    DETECTORS = [
        # Legacy strategies (kept for backward compatibility, low weight)
        ("ema20_pullback", ema20_signal, 0.1),
        ("ema_9_20", ema9_signal, 0.1),
        ("ema_crossover", ema_crossover_signal, 0.1),
        # ("smart_money", smart_money_signal, 0.1),  # optional legacy
        # Phase 1 detectors
        ("market_structure", get_market_structure_signal, MARKET_STRUCTURE_WEIGHT),
        ("bos", get_bos_signal, BOS_WEIGHT),
        ("choch", get_choch_signal, CHOCH_WEIGHT),
        # Phase 2 detectors
        ("sr_zones", get_sr_signal, SR_WEIGHT),
        ("fvg", get_fvg_signal, FVG_WEIGHT),
        # Phase 3.5 detectors
        ("fibonacci", get_fibonacci_signal, FIBONACCI_WEIGHT),
        # Phase 0 weighted detectors (if we want to use them later, we can add them here)
        # ("trend", ..., TREND_WEIGHT),
        # ("confirmation", ..., CONFIRMATION_WEIGHT),
        # ("breakout", ..., BREAKOUT_WEIGHT),
        # ("pullback", ..., PULLBACK_WEIGHT),
    ]

    detector_signals = []

    # ==========================================
    # DETECTOR EXECUTION AND SCORE AGGREGATION
    # ==========================================
    for detector_name, detector_func, weight in DETECTORS:
        try:
            # Call detector; it should return a Signal object
            signal = detector_func(df)
            # Ensure we have a Signal (legacy conversion not needed for new detectors)
            if not isinstance(signal, Signal):
                # If it's a legacy dict, convert
                signal = Signal.legacy(signal)
            signal.weight = weight
            detector_signals.append(signal)

        except Exception as e:
            # If a detector fails, continue with remaining detectors
            continue

    # ==========================================
    # DIRECTIONAL ALIGNMENT CHECK
    # ==========================================
    # Sum weights of detectors that agree on direction
    buy_weight = 0.0
    sell_weight = 0.0

    for signal in detector_signals:
        if signal.direction == "BUY":
            buy_weight += signal.weight
        elif signal.direction == "SELL":
            sell_weight += signal.weight

    # ==========================================
    # THRESHOLD AND FINAL DECISION
    # ==========================================
    # Calculate total score (sum of weighted scores)
    total_score = 0.0
    total_weight = 0.0
    for signal in detector_signals:
        total_score += signal.score * signal.weight
        total_weight += signal.weight

    # Avoid division by zero
    if total_weight > 0:
        average_score = total_score / total_weight
    else:
        average_score = 0.0

    # Determine final direction based on weighted alignment
    if buy_weight >= sell_weight and buy_weight > 0:
        final_direction = "BUY"
        # Confidence could be weighted average of confidence of BUY signals
        # For simplicity, we use proportion of buy weight
        final_confidence = min(100, int((buy_weight / (buy_weight + sell_weight)) * 100)) if (buy_weight + sell_weight) > 0 else 0
    elif sell_weight > buy_weight and sell_weight > 0:
        final_direction = "SELL"
        final_confidence = min(100, int((sell_weight / (buy_weight + sell_weight)) * 100)) if (buy_weight + sell_weight) > 0 else 0
    else:
        final_direction = "NEUTRAL"
        final_confidence = 0

    # Apply threshold
    if average_score >= CONFLUENCE_THRESHOLD and final_direction != "NEUTRAL":
        # Trade signal
        # Build reason chain from all signals that contributed to direction
        reason_parts = []
        for signal in detector_signals:
            if (final_direction == "BUY" and signal.direction == "BUY") or \
               (final_direction == "SELL" and signal.direction == "SELL"):
                reason_parts.append(f"{signal.detector}: {signal.reason}")
        reason = " | ".join(reason_parts) if reason_parts else f"{final_direction} signal"

        # For compatibility, we need to provide some legacy fields; we'll set them to None or default
        result = {
            "strategy": "Confluence Engine",
            "trend": final_direction,
            "signal": SignalEnum(final_direction),
            "confidence": final_confidence,
            "reason": reason,
            "setup_high": None,  # could be derived from meta later
            "setup_low": None,
            "entry_price": None,
        }
    else:
        # No trade
        reason = f"No trade: score {average_score:.1f} < threshold {CONFLUENCE_THRESHOLD} or direction neutral"
        result = {
            "strategy": "Confluence Engine",
            "trend": "NEUTRAL",
            "signal": SignalEnum.NO_TRADE,
            "confidence": 0,
            "reason": reason,
            "setup_high": None,
            "setup_low": None,
            "entry_price": None,
        }
    # Final safety gate: session and spread check
    if final_direction in ("BUY", "SELL"):
        if not trading_session():
            result["trend"] = "NEUTRAL"
            result["signal"] = SignalEnum.NO_TRADE
            result["reason"] = "Blocked: outside trading session"
        elif not spread_ok():
            result["trend"] = "NEUTRAL"
            result["signal"] = SignalEnum.NO_TRADE
            result["reason"] = "Blocked: spread too wide"
    return result