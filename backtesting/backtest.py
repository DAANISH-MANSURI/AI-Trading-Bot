import os
import sys
import MetaTrader5 as mt5
import pandas as pd

# ==========================================================
# Parent Folder
# ==========================================================

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# ==========================================================
# Imports
# ==========================================================

from config import SYMBOL, TIMEFRAME

from backtesting.historical_data import get_historical_data
from indicators import add_indicators
from strategy import get_signal
from stop_loss import calculate_sl_tp

from backtesting.trade_simulator import simulate_trade
from backtesting.performance import calculate_performance
from backtesting.account_simulator import AccountSimulator
from backtesting.position_sizer import calculate_position_size
from backtesting.trade_analytics import analyze_trades


# ==========================================================
# Main
# ==========================================================

def main():

    print("=" * 70)
    print("AI Trading Bot - Backtesting Engine")
    print("=" * 70)

    # ---------------------------------------
    # MT5 Connection
    # ---------------------------------------

    if not mt5.initialize():

        print("❌ MT5 Connection Failed")
        print(mt5.last_error())
        return

    account = AccountSimulator(
        starting_balance=10000,
        risk_percent=1
    )

    try:

        # ---------------------------------------
        # Load Historical Data
        # ---------------------------------------

        df = get_historical_data(
            symbol=SYMBOL,
            timeframe=TIMEFRAME,
            candles=5000
        )

        if df is None:

            print("❌ Failed To Load Historical Data")
            return

        print(f"✅ Loaded {len(df)} Candles")

        # ---------------------------------------
        # Indicators
        # ---------------------------------------

        df = add_indicators(df)

        print("✅ Indicators Calculated")

        # ---------------------------------------
        # Trade List
        # ---------------------------------------

        trades = []

        # ======================================
        # Single Position Engine
        # ======================================

        next_available_index = 200

        for i in range(200, len(df) - 1):

            # Wait until previous trade is closed
            if i < next_available_index:
                continue

            history = df.iloc[: i + 1].copy()

            signal = get_signal(history)

            if signal["signal"] == "NO_TRADE":
                continue

            # ---------------------------------------
            # Stop Loss / Take Profit
            # ---------------------------------------

            sl, tp = calculate_sl_tp(
                history,
                signal["signal"]
            )

            if sl is None:
                continue

            # ---------------------------------------
            # Position Size
            # ---------------------------------------

            lot = calculate_position_size(
                symbol=SYMBOL,
                balance=account.get_balance(),
                risk_percent=1,
                entry_price=history.iloc[-1]["close"],
                stop_loss=sl
            )

            # ---------------------------------------
            # Trade Simulation
            # ---------------------------------------

            result = simulate_trade(
                df,
                i,
                signal["signal"],
                sl,
                tp
            )

            if result is None:
                continue

            # ======================================
            # Prevent Overlapping Trades
            # ======================================

            next_available_index = result["exit_index"] + 1

            # ---------------------------------------
            # Extra Trade Information
            # ---------------------------------------

            result["sl"] = round(sl, 2)
            result["tp"] = round(tp, 2)
            result["lot_size"] = lot

            # ---------------------------------------
            # Account Update
            # ---------------------------------------

            account_info = account.process_trade(result)

            result["balance"] = account_info["balance"]
            result["profit"] = account_info["profit"]
            result["risk_amount"] = account_info["risk_amount"]

            trades.append(result)

        # ---------------------------------------
        # DataFrame
        # ---------------------------------------

        trades_df = pd.DataFrame(trades)
        print()
        print("=" * 70)
        print("SIGNAL SUMMARY")
        print("=" * 70)

        print(trades_df["signal"].value_counts())

        print("=" * 70)

        # ---------------------------------------
        # Performance
        # ---------------------------------------

        stats = calculate_performance(trades_df)

        # ---------------------------------------
        # Report
        # ---------------------------------------

        print()
        print("=" * 70)
        print("BACKTEST COMPLETED")
        print("=" * 70)

        print(f"Symbol         : {SYMBOL}")
        print(f"Timeframe      : {TIMEFRAME}")
        print(f"Total Trades   : {len(trades_df)}")

        print()

        print("=" * 70)
        print("PERFORMANCE REPORT")
        print("=" * 70)

        for key, value in stats.items():
            print(f"{key:<20}: {value}")

        print("=" * 70)

        # ---------------------------------------
        # Trade Analytics
        # ---------------------------------------

        analytics = analyze_trades(trades_df)

        print()

        print("=" * 70)
        print("TRADE ANALYTICS")
        print("=" * 70)

        for key, value in analytics.items():

          print(f"{key:<25}: {value}")

        print("=" * 70)

        # ---------------------------------------
        # Account Summary
        # ---------------------------------------

        print()

        print("=" * 70)
        print("ACCOUNT SUMMARY")
        print("=" * 70)

        print(f"Starting Balance : {account.starting_balance}")
        print(f"Final Balance    : {account.get_balance()}")

        print("=" * 70)

        # ---------------------------------------
        # Recent Trades
        # ---------------------------------------

        if not trades_df.empty:

            print("LAST 10 TRADES")
            print("=" * 70)

            print(trades_df.tail(10))

        else:

            print("⚠️ No Trades Found")

        # ---------------------------------------
        # Save CSV
        # ---------------------------------------

        os.makedirs("reports", exist_ok=True)

        trades_df.to_csv(
            "reports/backtest_results.csv",
            index=False
        )

        print()
        print("✅ Report Saved")
        print("reports/backtest_results.csv")

    finally:

        mt5.shutdown()

        print()
        print("✅ MT5 Connection Closed")


# ==========================================================
# Start
# ==========================================================

if __name__ == "__main__":
    main()