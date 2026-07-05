import time
import MetaTrader5 as mt5

from config.mt5 import SYMBOL
from config.trading import RISK_PERCENT
from mt5.market_data import get_market_data
from strategy.indicators import add_indicators
from strategy.strategy import get_signal
from risk.risk_manager import calculate_risk
from strategy.stop_loss import calculate_sl_tp
from utils.candle_watcher import is_new_candle
from live_trading.trade_logger import log_trade
from risk.lot_size import calculate_lot
from strategy.trade_filter import allow_buy, allow_sell
from strategy.spread_filter import spread_ok, get_spread
from strategy.session_filter import trading_session, current_session
from strategy.break_even import move_to_break_even
from strategy.trailing_stop import trailing_stop
from live_trading.position_manager import (
    has_open_position,
    get_position_type,
    wait_until_position_closed
)
from live_trading.execution_manager import (
    execute_buy,
    execute_sell,
    execute_close
)


from strategy.candle_patterns import (
    bullish_engulfing,
    bearish_engulfing,
    doji,
    pin_bar
)

# =====================================
# MT5 CONNECTION
# =====================================

if not mt5.initialize():
    print("❌ MT5 Connection Failed")
    quit()

account = mt5.account_info()

if account is None:
    print("❌ Account Login Failed")
    mt5.shutdown()
    quit()

print("=" * 60)
print("🚀 AI Trading Bot Started")
print("=" * 60)
print(f"Account      : {account.login}")
print(f"Name         : {account.name}")
print(f"Server       : {account.server}")
print(f"Balance      : ${account.balance}")
print(f"Trading Pair : {SYMBOL}")
print("=" * 60)

risk = calculate_risk(account.balance, RISK_PERCENT)

print(f"Risk Per Trade : ${risk:.2f}")

# =====================================
# MAIN LOOP
# =====================================

try:

    while True:

        # =====================================
        # GET MARKET DATA
        # =====================================

        df = get_market_data()

        if df is None:
            print("❌ Failed to get market data")
            time.sleep(5)
            continue

        # =====================================
        # ADD INDICATORS
        # =====================================

        df = add_indicators(df)

        # =====================================
        # CHECK NEW CANDLE
        # =====================================

        if is_new_candle(df):

            # Strategy Signal
            signal = get_signal(df)

            # Last Candle
            last = df.iloc[-1]
            atr = last["ATR"]

            # Position Check
            open_position = has_open_position(SYMBOL)
            position_type = get_position_type()

            # Stop Loss & Take Profit
            sl, tp = calculate_sl_tp(df, signal["signal"])

            # Trade Filters
            buy_allowed = allow_buy(df)
            sell_allowed = allow_sell(df)

            spread_allowed = spread_ok()
            spread = get_spread()

            session_allowed = trading_session()
            session_name = current_session()

            # Default Lot
            lot = 0.0

            # Calculate Lot Size
            if signal["signal"] in ["BUY", "SELL"] and sl is not None:

                lot = calculate_lot(
                    SYMBOL,
                    risk,
                    last["close"],
                    sl
                )
            # =========================
            # TEST MODE
            # =========================
            if (
                AUTO_TRADING
                and signal["signal"] in ["BUY", "SELL"]
                ):
                lot = 0.01

            # =====================================
            # PRINT BOT STATUS
            # =====================================

            print("\n")
            print("=" * 70)

            print(f"Time      : {last['time']}")
            print(f"Price     : {last['close']:.5f}")

            print(f"EMA5      : {last['EMA5']:.5f}")
            print(f"EMA9      : {last['EMA9']:.5f}")
            print(f"EMA13     : {last['EMA13']:.5f}")
            print(f"EMA21     : {last['EMA21']:.5f}")
            print(f"EMA200    : {last['EMA200']:.5f}")

            print(f"RSI        : {last['RSI']:.2f}")
            print(f"ATR        : {last['ATR']:.5f}")

            print("-" * 70)

            print(f"Trend          : {signal['trend']}")
            print(f"Signal         : {signal['signal']}")
            print(f"BUY Allowed    : {buy_allowed}")
            print(f"SELL Allowed   : {sell_allowed}")
            print(f"Spread         : {spread} points")
            print(f"Spread OK      : {spread_allowed}")
            print(f"Session        : {session_name}")
            print(f"Session OK     : {session_allowed}")
            print(f"Reason         : {signal['reason']}")
            print(f"Open Position  : {open_position}")
            print(f"Position Type  : {position_type}")

            print(f"Stop Loss      : {sl}")
            print(f"Take Profit    : {tp}")
            print(f"Lot Size       : {lot}")

            print("-" * 70)

            print(f"Bullish Engulfing : {bullish_engulfing(df)}")
            print(f"Bearish Engulfing : {bearish_engulfing(df)}")
            print(f"Doji              : {doji(df)}")
            print(f"Pin Bar           : {pin_bar(df)}")

            # =====================================
            # SAVE SIGNAL TO CSV
            # =====================================

            log_trade(
                SYMBOL,
                signal["trend"],
                signal["signal"],
                last["close"],
                sl,
                tp,
                lot,
                signal["reason"]
            )

            print("✅ Trade Logged Successfully")

            print("=" * 70)

            # =====================================
            # AUTOMATIC TRADING
            # =====================================
            if AUTO_TRADING:

                # BUY
                if (
                    signal["signal"] == "BUY"
                    and buy_allowed
                    and spread_allowed
                    and session_allowed
                    and lot > 0
                    and sl is not None
                    and tp is not None
                ):

                    # Already BUY
                    if position_type == "BUY":

                        print("🟡 BUY Position Already Open")
                        print("Skipping Trade...")

                    else:

                        # Assume no close needed
                        closed = True

                        if position_type == "SELL":

                            print("🔄 Closing SELL Position...")

                            close_result = execute_close()

                            print(close_result)

                            closed = wait_until_position_closed()

                        if not closed:

                            print("❌ Position Close Timeout")

                        else:

                            if position_type == "SELL":
                                print("✅ Position Closed Successfully")

                            print("🟢 Opening BUY Position...")

                            result = execute_buy(
                                lot,
                                sl,
                                tp
                        )

                        print(result)

                        log_trade(
                            SYMBOL,
                            signal["trend"],
                            "BUY EXECUTED",
                            last["close"],
                            sl,
                            tp,
                            lot,
                            "BUY Executed"
                        )
                # SELL
                elif (
                    signal["signal"] == "SELL"
                    and sell_allowed
                    and spread_allowed
                    and session_allowed
                    and lot > 0
                    and sl is not None
                    and tp is not None
                ):

                    # Already SELL
                    if position_type == "SELL":

                        print("🟡 SELL Position Already Open")
                        print("Skipping Trade...")

                    else:

                        # Assume no close needed
                        closed = True

                        if position_type == "BUY":

                            print("🔄 Closing BUY Position...")

                            close_result = execute_close()

                            print(close_result)

                            closed = wait_until_position_closed()

                            if not closed:

                                print("❌ Position Close Timeout")

                            else:

                                if position_type == "BUY":
                                    print("✅ Position Closed Successfully")

                                print("🔴 Opening SELL Position...")

                                result = execute_sell(
                                    lot,
                                    sl,
                                    tp
                                )

                                print(result)

                                log_trade(
                                    SYMBOL,
                                    signal["trend"],
                                    "SELL EXECUTED",
                                    last["close"],
                                    sl,
                                    tp,
                                    lot,
                                    "SELL Executed"
                            )

            else:

              print("⚪ Auto Trading Disabled")

        # =====================================
        # BREAK EVEN & TRAILING STOP
        # =====================================

        if open_position:

            be_result = move_to_break_even()

            if be_result is not None:
                print("\n🟢 Break Even Activated")
                print(be_result)

            ts_result = trailing_stop(atr)

            if ts_result is not None:
                print("\n🔵 Trailing Stop Updated")
                print(ts_result)

        time.sleep(1)

except KeyboardInterrupt:

    print("\n🛑 Bot Stopped By User")

finally:

    mt5.shutdown()

    print("✅ MT5 Connection Closed")