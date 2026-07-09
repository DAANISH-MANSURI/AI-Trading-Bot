Files Created:
- strategy/shared/sr_zones.py

Files Modified:
- strategy/shared/swing.py
- config/strategy.py
- strategy/strategy.py

Implementation Summary:
Phase 3 implements Support/Resistance (S/R) Zone Detection and integration:
1. Created strategy/shared/sr_zones.py with:
   - S/R zone clustering algorithm using single-linkage with price tolerance (SR_ZONE_CLUSTER_ATR × ATR or SR_ZONE_CLUSTER_PIPS × pips)
   - Maximum zone width cap (SR_MAX_ZONE_WIDTH_ATR × ATR) to prevent chaining
   - Zone validation requiring minimum touches (SR_MIN_TOUCHES)
   - Strength scoring formula combining touch count (40%), recency (30%), and average rejection wick size (30%)
   - Zone expiry based on SR_ZONE_EXPIRY_CANDLES and violation on close beyond zone
   - Signal generation for BUY (support rejection) or SELL (resistance rejection) when price shows wick-based rejection at zone edges
   - Helper functions for zone clustering, validation, and scoring
2. Enhanced strategy/shared/swing.py with:
   - Added get_swing_highs(df, lookback=SWING_LOOKBACK) function returning all swing high points as list of dicts with index and price
   - Added get_swing_lows(df, lookback=SWING_LOOKBACK) function returning all swing low points as list of dicts with index and price
   - Both functions reuse existing is_swing_high()/is_swing_low() logic rather than duplicating detection algorithm
3. Updated config/strategy.py with S/R zone configuration parameters:
   - SR_ZONE_CLUSTER_ATR, SR_ZONE_CLUSTER_PIPS: clustering tolerance
   - SR_MAX_TOUCHES_FOR_SCORE: touch count normalization
   - SR_ZONE_EXPIRY_CANDLES: zone max age
   - SR_WICK_NORMALIZER_ATR: wick size normalization factor
   - SR_MIN_TOUCHES: minimum touches for valid zone
   - SR_VIOLATION_ATR, SR_VIOLATION_PIPS: zone violation threshold
   - SR_MAX_ZONE_WIDTH_ATR: maximum zone width cap (prevents unreasonable chaining)
   - SR_WEIGHT: detector weight in confluence engine
4. Modified strategy/strategy.py to:
   - Import get_sr_signal from strategy.shared.sr_zones
   - Add SR_WEIGHT to config imports
   - Add S/R zone detector to Confluence Engine registry: ("sr_zones", get_sr_signal, SR_WEIGHT)
   - Positioned appropriately in the detector registry after other Phase 2 detectors

The implementation follows the Phase 0 Signal contract, maintains backward compatibility, and integrates cleanly with the Confluence Engine. S/R zone signals will be weighted by SR_WEIGHT in the final decision.

Manual Testing Steps:
1. Verify enhanced swing.py functions:
   ```python
   python3 -c "
   from strategy.shared.swing import get_swing_highs, get_swing_lows
   import pandas as pd
   df = pd.DataFrame({
       'high': [1.0, 1.2, 1.1, 1.3, 1.4, 1.35, 1.5],
       'low': [0.9, 1.0, 0.95, 1.1, 1.2, 1.15, 1.3],
       'close': [0.95, 1.1, 1.15, 1.0, 1.25, 1.35, 1.25],
       'ATR': [0.02]*7
   })
   highs = get_swing_highs(df)
   lows = get_swing_lows(df)
   print(f'Swing highs: {len(highs)}, Swing lows: {len(lows)}')
   ```
2. Verify S/R zone detection imports work (when dependencies available):
   ```python
   python3 -c "from strategy.shared.sr_zones import get_sr_signal; print('sr_zones import syntax OK')"
   ```
3. Verify configuration loads:
   ```python
   python3 -c "
   from config.strategy import (SR_ZONE_CLUSTER_ATR, SR_ZONE_CLUSTER_PIPS, SR_ZONE_EXPIRY_CANDLES,
                               SR_MIN_TOUCHES, SR_WEIGHT, SR_MAX_ZONE_WIDTH_ATR)
   print(f'SR Config: cluster_atr={SR_ZONE_CLUSTER_ATR}, cluster_pips={SR_ZONE_CLUSTER_PIPS}, expiry={SR_ZONE_EXPIRY_CANDLES}')"
   ```
4. Confirm sr_zones detector registered in Confluence Engine:
   ```bash
   grep -n "sr_zones.*get_sr_signal" strategy/strategy.py
   ```
5. Confirm no syntax errors in all modified files:
   ```bash
   python3 -m py_compile strategy/shared/swing.py strategy/shared/sr_zones.py config/strategy.py strategy/strategy.py
   ```

Verification Command Outputs:
```bash
$ grep -n "SR_" config/strategy.py
128:SR_ZONE_CLUSTER_ATR = 0.3           # cluster tolerance in ATR multiples (0 to disable)
129:SR_ZONE_CLUSTER_PIPS = 5            # cluster tolerance in pips (0 to disable)
130:SR_MAX_TOUCHES_FOR_SCORE = 10       # touch count for max score (normalization)
131:SR_ZONE_EXPIRY_CANDLES = 50         # max age of zone in candles
132:SR_WICK_NORMALIZER_ATR = 2.0        # ATR multiplier for wick normalization
133:SR_MIN_TOUCHES = 2                  # minimum touches for valid zone
134:SR_VIOLATION_ATR = 0.5              # violation size in ATR multiples (0 to disable)
135:SR_VIOLATION_PIPS = 3               # violation size in pips (0 to disable)
136:SR_MAX_ZONE_WIDTH_ATR = 3.0         # max zone width in ATR multiples (0 to disable)
137:SR_WEIGHT = 1.0                     # weight for SR zone detector in confluence engine

$ grep -n "sr_zones\|SR_WEIGHT\|get_sr_signal" strategy/strategy.py
16:from strategy.shared.sr_zones import get_sr_signal
29:    SR_WEIGHT,
64:        ("sr_zones", get_sr_signal, SR_WEIGHT),
```

Git Commit Message:
Implement Phase 3: Support/Resistance Zone Detection & Integration
- Added get_swing_highs and get_swing_lows to strategy/shared/swing.py for swing point enumeration
- Created strategy/shared/sr_zones.py with S/R zone detection, clustering, validation, and signal generation
- Enhanced S/R zone logic with single-linkage clustering, max width cap, and strength scoring (touch count + recency + wick size)
- Modified strategy/strategy.py to add S/R zone detector to Confluence Engine with SR_WEIGHT weight
- Added comprehensive S/R zone configuration to config/strategy.py including clustering tolerances, expiry rules, and violation thresholds
- Maintained backward compatibility; all modified modules compile without syntax errors