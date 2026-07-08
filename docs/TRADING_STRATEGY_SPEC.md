# AI Trading Bot V2
## Trading Strategy Specification
Version: 1.0 (Draft)

---

# 1. Goal

Build a professional, rule-based trading system that:

- Trades only high-probability setups.
- Avoids sideways markets.
- Has objective rules (no guessing).
- Works for both backtesting and live trading.
- Is easy to optimize later.

The strategy must never depend on emotions.

---

# 2. Trading Style

Type:
Swing Intraday Trend Following

Primary Market:
XAUUSD
BTCUSD
NAS100

Future:
Forex

---

# 3. Timeframe

Primary:
M15

Higher Timeframe Confirmation:
H1

Future:
M5 Scalping (Optional)

---

# 3.1 Execution Timeframes

Primary Timeframe (Execution): M15

Higher Timeframe Confirmation: H1 (Mandatory)

Rules:

- H1 trend must be Bullish for BUY.
- H1 trend must be Bearish for SELL.
- If H1 is Sideways → No Trade.
- Entries are executed only on M15.

---

# 4. Trend Definition

Trend is determined using EMA20.

Rules:

- Bullish: the current M15 close is above EMA20 and the EMA20 slope over the last 5 M15 candles is greater than $0.5 \times ATR(14)$.
- Bearish: the current M15 close is below EMA20 and the EMA20 slope over the last 5 M15 candles is less than $-0.5 \times ATR(14)$.
- Otherwise: No Trend. No trades.

---

# 5. Market Filter

Before looking for entries, the market must not be sideways.

Conditions:

- EMA20 slope magnitude over the last 5 M15 candles must be at least $0.5 \times ATR(14)$.
- ATR(14) must be above the configured minimum threshold for the instrument.
- The high-low range of the last 20 M15 candles must be greater than $0.8 \times ATR(14)$.

If any condition fails, the market is considered sideways and NO TRADE.

---

# 6. Entry Logic

Step 1

Trend exists.

↓

Step 2

Wait for a pullback of at least 1 M15 bar against the trend.

↓

Step 3

Price returns to within $0.5 \times ATR(14)$ of EMA20.

↓

Step 4

A confirmation candle appears that satisfies the rules in Section 7.

↓

Step 5

Break the high of the confirmation candle for a BUY or the low of the confirmation candle for a SELL.

↓

Enter trade at the breakout price plus 1 minimum price increment.

Never enter before breakout.

---

# 7. Confirmation Candle

BUY confirmation candle must satisfy one of the following:

- Bullish Engulfing: current candle body is larger than the previous candle body and the current candle closes above the previous candle close.
- Strong Bull Candle: candle body is at least 70% of the total candle range and the candle closes above its open.
- Hammer: lower wick is at least 2 times the candle body and the candle closes above its open.

SELL confirmation candle must satisfy one of the following:

- Bearish Engulfing: current candle body is larger than the previous candle body and the current candle closes below the previous candle close.
- Strong Bear Candle: candle body is at least 70% of the total candle range and the candle closes below its open.
- Shooting Star: upper wick is at least 2 times the candle body and the candle closes below its open.

---

# 8. Stop Loss

Stop Loss is placed:

- Below the confirmation candle low for a BUY.
- Above the confirmation candle high for a SELL.
- The stop is placed 1 minimum price increment beyond the selected level.

Never use a fixed SL.

---

# 9. Take Profit

No fixed TP.

Use dynamic exit.

---

# 10. Exit Rules

Exit only if one of the following occurs first:

- EMA9 closes across EMA20 on the current bar. For a BUY, EMA9 close must be above EMA20 close. For a SELL, EMA9 close must be below EMA20 close.
- Trailing stop level is hit.
- Market structure breaks. For a BUY, price closes below the most recent swing low. For a SELL, price closes above the most recent swing high.

---

# 11. Break Even

Move SL to entry when unrealized profit reaches $+1R$.

- $1R$ is equal to the initial stop distance in price units.
- Move the stop only once.

---

# 12. Trailing Stop

- For a BUY, trail the stop below the current EMA9 value.
- For a SELL, trail the stop above the current EMA9 value.
- Recalculate the trailing stop on each new M15 bar.
- Never move the stop backward.

---

# 13. Risk Management

- Risk per trade: 1% of account balance.
- Maximum daily loss: 3% of account balance.
- Maximum open trades: 1.
- If the daily loss limit is reached, no new trades are allowed until the next trading day.
- Position size must be calculated from balance, risk %, and stop distance.

---

# 14. Session Filter

Trade only during the London and New York sessions.

- London session: 08:00 to 16:00 server time.
- New York session: 13:00 to 21:00 server time.
- Avoid the Asian session.

---

# 15. News Filter

Do not trade from 30 minutes before to 30 minutes after any high-impact news event.

- Use the economic calendar feed.
- The event must be flagged as high impact.

---

# 16. Invalid Setup

Do NOT trade if:

- The market is sideways, as defined in Section 5.
- ATR(14) is below the configured minimum threshold for the instrument.
- The confirmation candle fails the rules in Section 7.
- EMA20 is flat, defined as the absolute slope over the last 5 bars being less than $0.5 \times ATR(14)$.
- Spread is above the configured maximum spread for the instrument.
- The current time is within the news filter window from Section 15.

---

# 17. Position Sizing

Risk-based.

Lot size is calculated from:

- Balance
- Risk %
- Stop Loss distance
- Instrument pip/point value

Round the result to the broker minimum lot increment.

---

# 18. Logging

Every trade must log:

Trend

Entry

SL

Exit

RR

Reason

Duration

Profit

---

# 19. Future Features

Liquidity Sweep

CHOCH

BOS

FVG

Order Blocks

AI Strategy Selection

Multi Timeframe

Optimizer

---

# 20. Golden Rule

The bot should prefer:

No Trade

instead of

Bad Trade.

