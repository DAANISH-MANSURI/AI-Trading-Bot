import MetaTrader5 as mt5

from config import SYMBOL, TIMEFRAME

from backtesting.models import BacktestResult
from backtesting.historical_data import get_historical_data

from strategy.indicators import add_indicators


def run_backtest(

    symbol=None,

    timeframe=None,

    parameters=None,

    starting_balance=10000,

    risk_percent=1,

    candles=5000

):

    # ==========================================
    # Default Values
    # ==========================================

    if symbol is None:
        symbol = SYMBOL

    if timeframe is None:
        timeframe = TIMEFRAME

    print()
    print("=" * 70)
    print("Running Backtest Engine...")
    print("=" * 70)

    # ==========================================
    # Load Historical Data
    # ==========================================

    df = get_historical_data(

        symbol=symbol,

        timeframe=timeframe,

        candles=candles

    )

    if df is None:

        print("❌ Failed To Load Historical Data")

        return None

    print(f"✅ Loaded {len(df)} Candles")

    # ==========================================
    # Indicators
    # ==========================================

    df = add_indicators(df)

    print("✅ Indicators Calculated")

    # ==========================================
    # Trade Container
    # ==========================================

    trades = []

    print("✅ Trade Container Ready")

    # ==========================================
    # Placeholder
    # ==========================================

    print("⏳ Trade Engine Coming In File 2.2")

    # ==========================================
    # Temporary Result
    # ==========================================

    result = BacktestResult(

        symbol=symbol,

        timeframe=str(timeframe),

        starting_balance=starting_balance,

        final_balance=starting_balance,

        trades=None,

        performance={},

        analytics={},

        drawdown={}

    )

    return result