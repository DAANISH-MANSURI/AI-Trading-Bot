Files Created:
- strategy/shared/fvg.py

Files Modified:
- strategy/shared/pullback.py
- config/strategy.py

Implementation Summary:
Phase 2 implements Fair Value Gap (FVG) detection and integration:
1. Created strategy/shared/fvg.py with:
   - FVG detection logic for 3-candle bullish/bearish imbalances
   - Validation rules (expiration, invalidation via opposite-side close)
   - Signal generation for FVG retracement touches (direction: BUY for bullish FVG, SELL for bearish FHG)
   - Dynamic scoring based on gap size (ATR-relative) and age (newer = higher score)
   - Helper function get_active_fvgs() for pullback integration
2. Modified strategy/shared/pullback.py to:
   - Import FVG detection from fvg.py
   - Expand pullback conditions to include FVG zones (OR condition with EMA20)
   - Check for price overlap with active FVGs of correct type (bullish for bullish pullback, bearish for bearish pullback)
   - Maintain all existing structure and risk controls
3. Updated config/strategy.py with FVG configuration:
   - FVG_MIN_GAP_PIPS: minimum gap size in pips
   - FVG_MIN_GAP_ATR: minimum gap size in ATR multiples
   - FVG_EXPIRY_CANDLES: max age of FVG in candles
   - All existing configuration preserved

The implementation follows the Phase 0 Signal contract, maintains backward compatibility, and integrates cleanly with the Confluence Engine. FVG signals will be weighted by FVG_WEIGHT (to be added in config/confluence engine weights in future phases, but structure is ready).

Manual Testing Steps:
1. Verify FVG detection:
   ```python
   python3 -c "
   from strategy.shared.fvg import get_active_fvgs, get_fvg_signal
   import pandas as pd
   df = pd.DataFrame({
       'high': [1.0, 1.2, 1.1, 1.3, 1.4, 1.35, 1.5],
       'low': [0.9, 1.0, 0.95, 1.1, 1.2, 1.15, 1.3],
       'close': [0.95, 1.1, 1.15, 1.0, 1.25, 1.35, 1.25, 1.45],
       'ATR': [0.02]*7
   })
   fvgs = get_active_fvgs(df)
   print('Active FVGs:', len(fvgs))
   if fvgs: print('First FVG:', fvgs[0])
   signal = get_fvg_signal(df)
   print('FVG Signal:', signal.direction, 'score:', signal.score)
   ```
2. Test pullback integration:
   ```python
   python3 -c "
   from strategy.shared.pullback import bullish_pullback, bearish_pullback
   import pandas as pd
   df = pd.DataFrame({
       'open': [1.0, 1.1, 1.05, 1.15, 1.2, 1.18, 1.25],
       'high': [1.02, 1.12, 1.07, 1.17, 1.22, 1.20, 1.27],
       'low': [0.98, 1.10, 1.03, 1.13, 1.18, 1.16, 1.23],
       'close': [1.0, 1.1, 1.05, 1.15, 1.2, 1.18, 1.25],
       'ATR': [0.02]*7,
       'EMA20': [1.0, 1.05, 1.08, 1.10, 1.13, 1.15, 1.18]
   })
   print('Bullish pullback:', bullish_pullback(df))
   print('Bearish pullback:', bearish_pullback(df))
   ```
3. Verify configuration loads:
   ```python
   python3 -c "
   from config.strategy import FVG_MIN_GAP_PIPS, FVG_MIN_GAP_ATR, FVG_EXPIRY_CANDLES
   print(f'FVG Config: min_pips={FVG_MIN_GAP_PIPS}, min_atr={FVG_MIN_GAP_ATR}, expiry={FVG_EXPIRY_CANDLES}')
   ```
4. Confirm no import errors in strategy.py:
   ```python
   python3 -c "
   from strategy.strategy import get_signal
   print('Strategy module imports successfully')
   ```
5. Check legacy strategy compatibility:
   ```python
   python3 -c "
   from strategy.strategies.ema20_pullback import get_signal as ema_signal
   import pandas as pd
   df = pd.DataFrame({'close':[1.0,1.1],'high':[1.02,1.12],'low':[0.98,1.08],'ATR':[0.02,0.02],'EMA20':[1.0,1.05]})
   print('Legacy EMA20 signal:', ema_signal(df)['signal'])
   ```

Git Commit Message:
Implement Phase 2: FVG Detection & Integration
- Created strategy/shared/fvg.py with FVG detection, validation, and signal generation
- Modified strategy/shared/pullback.py to use FVG zones as pullback/entry references
- Added FVG configuration parameters to config/strategy.py
- FVG detector returns Signal objects for retracement entries (BUY/SELL on touch)
- Pullback functions now accept EMA20 OR FVG zone as valid pullback conditions
- Maintained full backward compatibility with existing strategies and interfaces
- Production-ready implementation with error handling and configurable parameters