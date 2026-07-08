# MT5 Trading Bot — Complete Phase-Wise Roadmap

**Goal:** Rebuild the strategy engine around Smart Money Concepts (BOS, CHoCH, FVG, S/R zones), with chart visualization and a confluence-based decision system — replacing the single-indicator EMA20 pullback approach.

**How to use this doc:** Work through phases in order. Each phase lists exactly which existing files get modified and which new files need to be created. Don't skip ahead — each phase builds on the previous one's output.

---

## Phase 0: Architecture Foundation (Confluence Engine Design)

**Objective:** Redesign the core decision-making structure BEFORE building any detection logic, so every future module plugs into a stable contract.

**Files Modified:**
- `strategy/strategy.py` — becomes the central confluence engine
- `config/strategy.py` — add new config sections for SMC parameters (placeholders for now)

**Files to Review (not modified yet):**
- `strategy/shared/trend.py`
- `strategy/shared/confirmation.py`
- `strategy/session_filter.py`
- `strategy/spread_filter.py`
- `strategy/trade_filter.py`

**Deliverable:**
- A defined "Signal" data contract (direction, strength/score, reasoning string) that every detector will return
- A scoring/threshold system in `strategy.py` that decides when combined signals justify a trade
- A decision on what happens to old strategies (`ema20_pullback.py`, `ema_9_20.py`, `ema_crossover.py`, `breakout.py`, `smart_money.py`, `scalping.py`) — deprecate, archive, or keep as optional legacy modules

**Exit Criteria:** You can describe, in plain language, exactly how a trade signal will flow from raw price data → individual detectors → combined score → final entry decision — before any detector exists.

---

## Phase 1: Market Structure Engine (BOS / CHoCH)

**Objective:** Detect break of structure and change of character using pure price action (no fake volume-based logic).

**Files Modified:**
- `strategy/shared/market_structure.py` — add BOS/CHoCH detection functions
- `strategy/shared/swing.py` — extend swing point output if needed (e.g., labeling swings as HH/HL/LH/LL)

**New Files:**
- None required yet — this phase extends existing modules only

**Config Additions (`config/strategy.py`):**
- Swing lookback period
- BOS confirmation rule (close-based vs wick-based)
- Minimum structure break size (in pips/ATR) to filter noise

**Deliverable:** Functions that return standardized Signal objects (per Phase 0 contract) indicating trend structure state and any fresh BOS/CHoCH.

**Exit Criteria:** Manually verify against 10-15 real chart examples (different sessions, different volatility) that detected BOS/CHoCH match what you'd mark by eye.

---

## Phase 2: Fair Value Gap (FVG) Detection

**Objective:** Detect 3-candle imbalance gaps and track whether price has retested them.

**Files Modified:**
- `strategy/shared/pullback.py` — integrate FVG zones as a valid pullback/entry reference point

**New Files:**
- `strategy/shared/fvg.py` — dedicated FVG detection module (detection, gap classification bullish/bearish, mitigation/retest tracking)

**Config Additions (`config/strategy.py`):**
- Minimum FVG size threshold (to ignore insignificant gaps)
- FVG expiry (how many candles before an unfilled FVG is considered invalid)

**Deliverable:** A function returning active FVG zones with price levels, direction, and mitigation status — as a Signal object.

**Exit Criteria:** Cross-check detected FVGs visually on a few charts to confirm they match standard SMC definition (gap between candle 1 high/low and candle 3 low/high).

---

## Phase 3: Support/Resistance Zone Detection

**Objective:** Identify S/R as strength-scored zones (not single lines), based on swing point clustering and touch count.

**New Files:**
- `strategy/shared/sr_zones.py` — zone detection, clustering nearby swing levels, strength scoring (touch count, recency, rejection wick size)

**Files Modified:**
- `strategy/shared/market_structure.py` — may feed swing data into `sr_zones.py`

**Config Additions (`config/strategy.py`):**
- Zone clustering distance (in pips/ATR)
- Minimum touches to qualify as a valid zone
- Zone decay/expiry rules

**Deliverable:** Function returning active S/R zones with a strength score, usable by the confluence engine to check "is price near a significant zone."

**Exit Criteria:** Zones visually match areas where price has historically reacted multiple times — not just any random swing point.

---

## Phase 4: Chart Visualization Layer

**Objective:** Draw everything detected (BOS/CHoCH, FVG, S/R, trend lines) directly onto the live MT5 chart for verification and debugging.

**New Files:**
- `mt5/chart_drawer.py` — wraps `mt5.ObjectCreate()` calls: rectangles for FVG, horizontal/zone rectangles for S/R, labeled arrows/text for BOS/CHoCH, trend lines from swing points

**Files Modified:**
- `mt5/mt5_connector.py` — expose chart object management (create/update/delete) if not already present

**Deliverable:** Bot automatically annotates the live chart in real time as it identifies structure — this becomes your primary debugging tool for the next phases.

**Exit Criteria:** Watching the live chart, everything the bot "believes" is happening (structure breaks, gaps, zones) is visibly drawn and matches your own reading of price action.

---

## Phase 5: Confluence Integration (Wiring Everything Together)

**Objective:** Connect Phase 1-3 detectors into the Phase 0 confluence engine to produce actual entry signals.

**Files Modified:**
- `strategy/strategy.py` — call all detectors, apply scoring/threshold logic from Phase 0
- `strategy/trade_filter.py` — final gate combining structure + FVG + S/R + session + spread filters
- `config/strategy.py` — add confluence threshold value, per-signal weightings

**Deliverable:** A single entry decision function that only fires when combined score crosses your defined threshold — e.g., HTF trend + BOS confirmation + FVG retest + S/R proximity + session filter all aligning.

**Exit Criteria:** Backtest-ready — the strategy produces a manageable number of signals per day (your target: 2-3), each with a clear multi-factor justification.

---

## Phase 6: Risk Management Upgrade

**Objective:** Make position sizing and stop placement SMC-aware and volatility-adjusted.

**Files Modified:**
- `risk/risk_manager.py` — add structure-based stop-loss placement (beyond last swing/order block), ATR-based dynamic sizing
- `risk/lot_size.py` — adjust sizing logic to account for structure-based SL distance
- `strategy/stop_loss.py` — SL rules referencing BOS/CHoCH invalidation points instead of fixed pip distance

**Deliverable:** Every trade's SL/TP is derived from actual market structure (last swing point, FVG boundary) rather than arbitrary fixed distances.

**Exit Criteria:** Risk-reward ratios are consistent and every stop has a structural (not arbitrary) justification.

---

## Phase 7: Backtesting Validation

**Objective:** Rigorously test the new confluence-based strategy using your existing backtesting engine — no new modules needed, just proper usage.

**Files Used (already exist, no major changes expected):**
- `backtesting/backtest_engine.py`
- `backtesting/trade_engine.py`
- `backtesting/statistics_engine.py`
- `backtesting/performance.py`
- `backtesting/report_generator.py`

**Possible Modifications:**
- `backtesting/historical_data.py` — ensure it can supply multi-timeframe data (needed for HTF trend bias + LTF entries)

**Deliverable:** Walk-forward tested results — train on one period, validate on unseen data, across at least 2-3 different market regimes (trending, ranging, high volatility).

**Exit Criteria:** Strategy shows positive expectancy consistently across multiple out-of-sample periods, not just one curve-fit backtest run.

---

## Phase 8: Explainability & Logging

**Objective:** Every trade should log WHY it was taken — full reasoning trail, not just entry/exit prices.

**Files Modified:**
- `live_trading/trade_logger.py` — extend to log the full Signal reasoning chain (which detectors fired, scores, final decision)
- `trade_log.csv` structure — add columns for structure state, FVG status, S/R proximity, confluence score at entry

**Deliverable:** You can open any past trade and see exactly which conditions triggered it — critical for debugging losing trades and building trust in the system.

---

## Phase 9: Live Trading Integration

**Objective:** Wire the finished strategy into the live execution pipeline.

**Files Modified:**
- `live_trading/main.py` — use new `strategy.py` confluence engine
- `live_trading/trade_executor.py`
- `live_trading/order_manager.py`
- `live_trading/execution_manager.py`
- `live_trading/position_manager.py`

**No major new files expected here** — this phase is integration, not new logic.

**Deliverable:** Bot runs live (on demo account first) using the full SMC confluence pipeline, drawing on chart in real time, logging full reasoning per trade.

---

## Phase 10: Demo Forward Testing & Monitoring

**Objective:** Validate in real market conditions before risking real capital.

**No code changes expected** — this is observation and iteration:
- Run on demo for minimum 4-6 weeks
- Track win rate, expectancy, drawdown against backtest expectations
- Use Phase 8 logging to diagnose any live-vs-backtest divergence
- Only after consistent demo performance, consider small live capital

---

## Summary Table

| Phase | Focus | Key New Files | Key Modified Files |
|---|---|---|---|
| 0 | Architecture/contract | — | strategy.py, config/strategy.py |
| 1 | BOS/CHoCH | — | market_structure.py, swing.py |
| 2 | FVG | shared/fvg.py | pullback.py |
| 3 | S/R zones | shared/sr_zones.py | market_structure.py |
| 4 | Chart drawing | mt5/chart_drawer.py | mt5_connector.py |
| 5 | Confluence wiring | — | strategy.py, trade_filter.py |
| 6 | Risk upgrade | — | risk_manager.py, lot_size.py, stop_loss.py |
| 7 | Backtesting | — | historical_data.py (maybe) |
| 8 | Explainability | — | trade_logger.py |
| 9 | Live integration | — | live_trading/* |
| 10 | Demo testing | — | (no code) |

---

## Working Principle Throughout

At the start of every phase, give Claude Code a prompt like:

```
We are on Phase [X]: [objective]. Only modify/create the files listed 
for this phase. Do not touch files from other phases. Give me a 
blueprint of the exact logic before writing code.
```

This keeps each phase isolated, reviewable, and prevents scope creep — which is what caused the original EMA20 strategy to be a black box that failed silently in live markets.
