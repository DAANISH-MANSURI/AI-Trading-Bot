from core.exceptions import (
    BacktestError,
    MT5ConnectionError
)

from config.backtesting import (
    DEFAULT_BALANCE,
    DEFAULT_RISK
)

from utils.logger import logger
import os
import sys
import MetaTrader5 as mt5

# ==========================================================
# Parent Folder
# ==========================================================

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# ==========================================================
# Imports
# ==========================================================

from config import SYMBOL, TIMEFRAME

from backtesting.historical_data import get_historical_data
from strategy.indicators import add_indicators

from backtesting.account_simulator import AccountSimulator
from backtesting.trade_engine import execute_trade_loop
from backtesting.statistics_engine import calculate_statistics
from backtesting.report_engine import save_reports


# ==========================================================
# Main
# ==========================================================

def main():

    print("=" * 70)
    print("AI Trading Bot - Backtesting Engine")
    logger.info("Backtesting Started")
    print("=" * 70)

    if not mt5.initialize():

        raise MT5ConnectionError(

        str(mt5.last_error())

    )

    try:

        # ==========================================
        # Account
        # ==========================================

        account = AccountSimulator(

            starting_balance=DEFAULT_BALANCE,

            risk_percent=DEFAULT_RISK

        )

        # ==========================================
        # Historical Data
        # ==========================================

        df = get_historical_data(

            symbol=SYMBOL,

            timeframe=TIMEFRAME,

            candles=5000

        )

        if df is None:

            print("❌ Failed To Load Historical Data")

            return

        print(f"✅ Loaded {len(df)} Candles")
        logger.info(f"Loaded {len(df)} Candles")

        # ==========================================
        # Indicators
        # ==========================================

        df = add_indicators(df)

        print("✅ Indicators Calculated")
        logger.info("Indicators Calculated")

        # ==========================================
        # Execute Trade Engine
        # ==========================================

        trades_df = execute_trade_loop(

            df=df,

            symbol=SYMBOL,

            account=account,

            risk_percent=DEFAULT_RISK

        )

        if trades_df.empty:

            print("⚠️ No Trades Found")

            return

        # ==========================================
        # Statistics
        # ==========================================

        statistics = calculate_statistics(
            trades_df,
            account.starting_balance
            )

        performance = statistics["performance"]

        analytics = statistics["analytics"]

        drawdown = statistics["drawdown"]

        # ==========================================
        # Console Report
        # ==========================================

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

        for key, value in performance.items():

            print(f"{key:<20}: {value}")

        print("=" * 70)

        print()

        print("=" * 70)
        print("TRADE ANALYTICS")
        print("=" * 70)

        for key, value in analytics.items():

            print(f"{key:<25}: {value}")

        print("=" * 70)

        print()

        print("=" * 70)
        print("ACCOUNT SUMMARY")
        print("=" * 70)

        print(f"Starting Balance : {account.starting_balance}")

        print(f"Final Balance    : {account.get_balance()}")

        print("=" * 70)

        print("LAST 10 TRADES")
        print("=" * 70)

        print(trades_df.tail(10))

        # ==========================================
        # Reports
        # ==========================================

        report_files = save_reports(

            trades_df,

            performance,

            analytics,

            drawdown

        )

        print()
        print("✅ Reports Generated")
        print(f"CSV          : {report_files['csv']}")
        print(f"Equity Curve : {report_files['equity_curve']}")
        print(f"HTML Report  : {report_files['html']}")

    except BacktestError as e:

        logger.error(str(e))

        print()

        print("❌ BACKTEST ERROR")

        print(e)

    except MT5ConnectionError as e:

        logger.error(str(e))

        print()

        print("❌ MT5 ERROR")

        print(e)

    except Exception as e:

        logger.exception(e)

        print()

        print("❌ UNKNOWN ERROR")

        print(e)

    finally:

        mt5.shutdown()

        print()

        print("✅ MT5 Connection Closed")
        logger.info("Backtesting Finished")


# ==========================================================
# Start
# ==========================================================

if __name__ == "__main__":

    main()