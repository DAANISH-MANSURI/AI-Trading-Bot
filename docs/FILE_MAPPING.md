# AI Trading Bot
# FILE_MAPPING.md

Version: 1.0 Draft

Status: Under Review

---

# Purpose

This document defines the responsibility of every source file.

Rules:

- One file = One responsibility
- No duplicate logic
- No hidden business logic
- No unnecessary files
- Every module must be reusable

---

# PROJECT STRUCTURE

```
AI-Trading-Bot/

config/
core/
docs/
mt5/
strategy/
risk/
backtesting/
live_trading/
reports/
tests/
```

---

# CONFIG

## config/trading.py

Purpose

Trading configuration.

Contains

- Risk %
- RR
- Timeframes
- Trading Sessions
- Symbol
- Magic Number

Must NOT

Contain trading logic.

---

## config/backtesting.py

Purpose

Backtesting configuration.

Contains

- Starting Balance
- Commission
- Spread
- Slippage

---

# MT5

## mt5/market_data.py

Purpose

Load market data.

Responsibilities

- Historical candles
- Live candles
- Data validation

Must NOT

Generate signals.

---

## mt5/symbol_info.py

Purpose

Broker information.

Responsibilities

- Digits
- Point
- Tick Size
- Stop Level
- Lot Limits

---

# STRATEGY

## strategy/indicators.py

Purpose

Calculate indicators.

Responsibilities

- EMA
- ATR
- RSI

Must NOT

Generate trades.

---

## strategy/shared/trend.py

Purpose

Trend detection.

Returns

Bullish

Bearish

Sideways

---

## strategy/shared/pullback.py

Purpose

Detect EMA20 pullback.

---

## strategy/shared/confirmation.py

Purpose

Confirmation candle detection.

---

## strategy/shared/filter.py

Purpose

Trading filters.

Responsibilities

- ATR Filter
- Session Filter
- Spread Filter
- Sideways Filter

---

## strategy/strategies/ema20_pullback.py

Purpose

Main strategy.

Consumes

Trend

↓

Pullback

↓

Confirmation

↓

Generate WAIT_BUY / WAIT_SELL

Must NOT

Execute trades.

---

## strategy/stop_loss.py

Purpose

Calculate Stop Loss and Take Profit.

---

# RISK

## risk/position_sizer.py

Purpose

Lot calculation.

---

## risk/risk_manager.py

Purpose

Risk validation.

Responsibilities

- Risk per trade
- Daily loss limit
- Max open trades
- Daily pause

---

# BACKTESTING

## backtesting/trade_engine.py

Purpose

Backtest execution engine.

Responsibilities

- Read strategy signal
- Manage pending setups
- Execute trades
- Update account

Must NOT

Contain strategy logic.

---

## backtesting/trade_simulator.py

Purpose

Trade simulation.

Responsibilities

- Simulate SL
- Simulate TP
- Simulate trailing
- Simulate exits

---

## backtesting/account_simulator.py

Purpose

Virtual account.

Responsibilities

- Balance
- Equity
- Profit
- Drawdown

---

## backtesting/statistics_engine.py

Purpose

Performance calculation.

---

## backtesting/report_engine.py

Purpose

Generate reports.

Outputs

CSV

HTML

Equity Curve

---

# LIVE TRADING

## live_trading/main.py

Purpose

Live execution loop.

---

## live_trading/order_manager.py

Purpose

Send orders.

---

## live_trading/position_manager.py

Purpose

Manage open positions.

---

# REPORTS

Purpose

Generated files only.

Contains

- CSV
- HTML
- PNG

Must NOT

Contain source code.

---

# TESTS

Purpose

Unit tests.

Never modify production code.

---

# MODULE DEPENDENCY

```
Market Data

↓

Indicators

↓

Filters

↓

Trend

↓

Pullback

↓

Confirmation

↓

Strategy

↓

Stop Loss

↓

Risk

↓

Trade Engine

↓

Trade Simulator

↓

Reports
```

No module may depend on a future layer.

---

# FILE CREATION RULES

A new file may be created ONLY IF:

1. Existing files cannot hold the responsibility.

AND

2. Approval has been given.

Otherwise,

Reuse existing modules.

---

# FILE MODIFICATION RULES

Before modifying any file:

1. Verify its responsibility.

2. Confirm the change belongs to that responsibility.

3. Never add unrelated logic.

---

# DUPLICATE LOGIC

Duplicate logic is forbidden.

If functionality already exists,

reuse it.

Do not create another implementation.

---

# ARCHITECTURE RULE

If any implementation conflicts with:

- TRADING_STRATEGY_SPEC.md
- ARCHITECTURE_SPEC.md
- FILE_MAPPING.md

The implementation must be rejected until the documents are updated first.