from dataclasses import dataclass
from typing import Dict, Any, Optional
from enum import Enum
from core.enums import Signal as SignalEnum

@dataclass
class Signal:
    """
    Standardized Signal contract for all detectors.
    Used by the Confluence Engine to communicate between detectors and decision-making.
    """
    detector: str  # Name of the detector that produced this signal
    direction: str  # "BUY", "SELL", or "NEUTRAL"
    score: float  # Strength score (0-100)
    confidence: int  # Certainty level (0-100)
    reason: str  # Human readable explanation
    meta: Dict[str, Any]  # Optional structured metadata from the detector
    timestamp: int  # Bar index or timestamp
    weight: float  # Relative weight of this detector (for scoring)

    @staticmethod
    def legacy(signal_dict: Dict) -> 'Signal':
        """
        Convert legacy dict format to Signal class.
        Used to maintain backward compatibility.
        Args:
            signal_dict: Dict with legacy format keys
        Returns: Signal object
        """
        return Signal(
            detector=signal_dict.get("detector", "legacy"),
            direction=signal_dict["signal"].value if isinstance(signal_dict.get("signal"), SignalEnum) else signal_dict.get("signal", "NO_TRADE"),
            score=signal_dict.get("confidence", 0),
            confidence=signal_dict.get("confidence", 0),
            reason=signal_dict.get("reason", ""),
            meta={},
            timestamp=signal_dict.get("timestamp", 0),
            weight=1.0
        )