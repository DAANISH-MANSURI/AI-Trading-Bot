"""
Strategy Router
"""

from strategy.shared.signal import Signal
from strategy.strategies.ema20_pullback import get_signal as ema20_signal
from strategy.strategies.ema_9_20 import get_signal as ema9_signal
from strategy.strategies.ema_crossover import get_signal as ema_crossover_signal
from strategy.strategies.smart_money import get_signal as smart_money_signal

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
    # ==========================================
    # PHASE 0: INITIALIZE STRUCTURE
    # ==========================================
    # Detector registry with weights (to be loaded from config in future)
    DETECTORS = [
        # Current detectors - all with minimal weight until they provide Signal objects
        ("ema20_pullback", ema20_signal, 0.1),  # weight 0.1 (legacy fallback)
        ("ema_9_20", ema9_signal, 0.1),         # weight 0.1
        ("ema_crossover", ema_crossover_signal, 0.1),  # weight 0.1
        # ("smart_money", smart_money_signal, 0.1),  # weight 0.1 (will be uncommented later)
    ]

    # Load weights and defaults from config for Phase 0 configuration
    # These are placeholder values that will be overridden when config is ready
    CONFLUENCE_THRESHOLD = 70  # placeholder - will be moved to config/strategy.py
    COUNTER_TREND_FACTOR = 0.8  # multiplier for signals opposing HTF trend
    detector_signals = []

    # ==========================================
    # DETECTOR EXECUTION AND SCORE AGGREGATION
    # ==========================================
    for detector_name, detector_func, weight in DETECTORS:
        try:
            # Call each legacy strategy to maintain compatibility
            # It returns a legacy dict, which we convert to Signal
            legacy_signal = detector_func(df)

            # Convert to Signal format for consistency with future detectors
            converted_signal = Signal.legacy(legacy_signal)
            converted_signal.weight = weight

            # Extract dimensions needed for direction alignment
            signal_direction = converted_signal.direction
            detector_signals.append((converted_signal, weight))

        except Exception as e:
            # If a detector fails, continue with remaining detectors
            continue

    # ==========================================
    # DIRECTIONAL ALIGNMENT CHECK
    # ==========================================
    # Sum weights of detectors that agree on direction
    buy_weight = 0.0
    sell_weight = 0.0

    for signal, weight in detector_signals:
        if signal.direction == "BUY":
            buy_weight += weight
        elif signal.direction == "SELL":
            sell_weight += weight

    # ==========================================
    # THRESHOLD AND FINAL DECISION
    # ==========================================
    # Calculate total score (simple sum of weights for now - will use scored signals later)
    total_score = buy_weight + sell_weight

    # Determine final direction
    if buy_weight >= sell_weight and buy_weight > 0:
        final_direction = "BUY"
        final_confidence = min(100, int(buy_weight * 100))  # simple scaling
    elif sell_weight > buy_weight and sell_weight > 0:
        final_direction = "SELL"
        final_confidence = min(100, int(sell_weight * 100))
    else:
        final_direction = "NO_TRADE"
        final_confidence = 0

    # Reset final_score for now (placeholder - 0-100 scale)
    final_score = 0 if final_direction == "NO_TRADE" else 70  # placeholder threshold met

    # ==========================================
    # FORMAT OUTPUT TO MATCH LEGACY INTERFACE
    # ==========================================
    result = {
        "strategy": "Confluence Engine",
        "trend": final_direction,
        "signal": SignalEnum(final_direction),
        "confidence": final_confidence,
        "reason": f"Phase 0 placeholder - Direction: {final_direction}, Score: {final_score}",
        "setup_high": None,
        "setup_low": None,
        "entry_price": None
    }

    return result
