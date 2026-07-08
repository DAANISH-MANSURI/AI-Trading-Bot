# AI Trading Bot
# ARCHITECTURE_SPEC.md

Version: 1.0 Draft

Status: Under Review

---

# 1. Purpose

This document defines the architecture of the AI Trading Bot.

It specifies:

- Execution flow
- Module responsibilities
- Data flow
- Folder structure
- Coding principles

This document does NOT contain implementation details.

---

# 2. System Overview

```
                 MT5
                  │
                  ▼
          Historical / Live Data
                  │
                  ▼
             Indicator Engine
                  │
                  ▼
            Market Filters
                  │
                  ▼
           Trend Detection
                  │
                  ▼
          Pullback Detection
                  │
                  ▼
       Confirmation Detection
                  │
                  ▼
             Entry Engine
                  │
                  ▼
           Position Sizing
                  │
                  ▼
            Trade Engine
                  │
                  ▼
          Trade Simulator
                  │
                  ▼
             Exit Engine
                  │
                  ▼
         Reports / Analytics
```

---

# 3. Execution Flow

The bot executes in the following order:

1. Load Market Data
2. Calculate Indicators
3. Apply Filters
4. Detect Trend
5. Detect Pullback
6. Detect Confirmation
7. Validate Entry
8. Calculate Stop Loss
9. Calculate Position Size
10. Execute Trade
11. Manage Trade
12. Generate Reports

The order must never change without approval.

---

# 4. Module Responsibilities

## Market Data

Responsibilities

- Load MT5 data
- Validate candles
- Return DataFrame
- Supports Primary Timeframe
- Supports Higher Timeframe Confirmation

The architecture must support strategies that require one or more higher timeframes for confirmation.

Must NOT

- Generate signals
- Calculate risk
- Execute trades

---

## Indicator Engine

Responsibilities

- EMA
- ATR
- RSI
- Other indicators

Must NOT

- Generate entries
- Detect trend

---

## Market Filter

Responsibilities

- Sideways detection
- ATR filter
- Session filter
- Spread filter
- News filter

Must NOT

- Generate signals

---

## Trend Engine

Responsibilities

- Detect Bullish Trend
- Detect Bearish Trend
- Detect No Trend

Must NOT

- Execute trades

---

## Pullback Engine

Responsibilities

Detect valid EMA20 pullback.

Must NOT

Generate entries.

---

## Confirmation Engine

Responsibilities

Detect confirmation candle.

Must NOT

Generate trades.

---

## Entry Engine

Responsibilities

Validate complete setup.

Generate:

BUY

SELL

NO TRADE

Must NOT

Calculate lot size.

---

## Stop Loss Engine

Responsibilities

Calculate SL.

Must NOT

Calculate lot size.

---

## Position Size Engine

Responsibilities

Calculate lot.

Must NOT

Generate entries.

---

## Trade Engine

Responsibilities

Manage complete trade lifecycle.

Must:

Open trades

Close trades

Prevent overlapping trades

---

## Trade Simulator

Responsibilities

Simulate historical trades.

Must NOT

Connect to MT5.

---

## Exit Engine

Responsibilities

Break Even

Trailing Stop

EMA Exit

Manual Exit

---

## Report Engine

Responsibilities

Performance

Drawdown

Analytics

Charts

HTML Report

CSV Report

---

# 5. Folder Responsibilities

backtesting/

Historical simulation only.

Never execute live orders.

---

live_trading/

Live MT5 execution only.

Never simulate trades.

---

strategy/

Contains only trading logic.

No MT5 code allowed.

---

risk/

Contains only risk management.

No strategy logic allowed.

---

mt5/

Contains only broker communication.

No strategy logic allowed.

---

reports/

Generated files only.

Never contains source code.

---

config/

Configuration only.

Never contains logic.

---

docs/

Documentation only.

---

# 6. Design Principles

Rule 1

One responsibility per module.

---

Rule 2

No duplicate logic.

---

Rule 3

No circular imports.

---

Rule 4

No unnecessary folders.

---

Rule 5

No placeholder files.

---

Rule 6

One source of truth.

---

Rule 7

Every module must be testable.

---

Rule 8

Every module must be reusable.

---

Rule 9

No MT5 code inside strategy.

---

Rule 10

No business logic inside reports.

---

# 7. Dependencies

Execution order:

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

Entry

↓

Risk

↓

Trade Engine

↓

Exit

↓

Reports

Modules may depend only on previous layers.

Never on future layers.

---

# 8. Future Extensions

Future modules may include:

- BOS
- CHOCH
- FVG
- Liquidity Sweep
- Order Blocks
- AI Strategy Selector
- Optimizer

These modules must plug into the architecture without redesigning it.

---

# 9. Golden Rules

The architecture must remain:

Simple

Modular

Reusable

Testable

Maintainable

Scalable

No architectural changes are allowed without updating this document first.