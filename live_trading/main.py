from signal import signal
import time
import MetaTrader5 as mt5

from core.enums import Signal
from config.mt5 import SYMBOL
from config.trading import RISK_PERCENT, AUTO_TRADING
from mt5.market_data import get_market_data
from strategy.indicators import add_indicators
from strategy.strategy import get_signal
from strategy.stop_loss import calculate_sl_tp
from strategy.trade_filter import allow_buy, allow_sell
from strategy.spread_filter import spread_ok, get_spread
from strategy.session_filter import trading_session, current_session
from strategy.break_even import move_to_break_even
from strategy.trailing_stop import trailing_stop
from strategy.candle_patterns import bullish_engulfing, bearish_engulfing, doji, pin_bar
from risk.risk_manager import calculate_risk
from risk.lot_size import calculate_lot
from utils.candle_watcher import is_new_candle
from live_trading.trade_logger import log_trade
from live_trading.position_manager import has_open_position, get_position_type, wait_until_position_closed
from live_trading.execution_manager import execute_buy, execute_sell, execute_close


def main():
    # =====================================
    # MT5 Connection
    # =====================================

    if not mt5.initialize():
        print("❌ MT5 Connection Failed")
        return

    account = mt5.account_info()

    if account is None:
        print("❌ Account Login Failed")
        mt5.shutdown()
        return

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

    try:
        while True:
            # ===============================
            # Get Market Data
            # ===============================
            df = get_market_data()

            if df is None:
                print("❌ Failed To Load Market Data")
                time.sleep(5)
                continue

            # ===============================
            # Indicators
            # ===============================
            df = add_indicators(df)

            # ===============================
            # New Candle
            # ===============================
            if not is_new_candle(df):
                time.sleep(1)
                continue

            last = df.iloc[-1]
            atr = last["ATR"]

            # ===============================
            # Strategy
            # ===============================
            signal = get_signal(df)

            # ===============================
            # Position
            # ===============================
            open_position = has_open_position(SYMBOL)
            position_type = get_position_type()

            # ===============================
            # Stop Loss
            # ===============================
            sl, tp = calculate_sl_tp(
                df,
                signal["signal"]
            )

            # ===============================
            # Filters
            # ===============================
            buy_allowed = allow_buy(df)
            sell_allowed = allow_sell(df)
            spread_allowed = spread_ok()
            spread = get_spread()
            #session_allowed = trading_session()
            session_allowed = True
            #session_name = current_session()
            session_name = "ALL"

            # ===============================
            # Lot Size
            # ===============================
            lot = 0.0
            if signal["signal"] in [Signal.BUY, Signal.SELL] and sl is not None:
                lot = calculate_lot(SYMBOL, risk, last["close"], sl)

            # TEST MODE
            if AUTO_TRADING and signal["signal"] in [Signal.BUY, Signal.SELL]:
                lot = max(lot, 0.01)

            print()
            print("=" * 70)
            print(f"Time      : {last['time']}")
            print(f"Price     : {last['close']:.5f}")
            print(f"EMA9      : {last['EMA9']:.5f}")
            print(f"EMA20     : {last['EMA20']:.5f}")
            print(f"RSI        : {last['RSI']:.2f}")
            print(f"ATR        : {last['ATR']:.5f}")
            print("-" * 70)
            print(f"Trend          : {signal['trend']}")
            #structure = signal["structure"]

            #print(f"Structure Score : {structure['score']}")
            #print(f"Bullish Structure : {structure['bullish_structure']}")
            #print(f"Bearish Structure : {structure['bearish_structure']}")
           # print(f"Bullish BOS : {structure['bullish_bos']}")
           # print(f"Bearish BOS : {structure['bearish_bos']}")
            print(f"Signal         : {signal['signal']}")
            print(f"BUY Allowed    : {buy_allowed}")
            print(f"SELL Allowed   : {sell_allowed}")
            print(f"Spread         : {spread} points")
            print(f"Spread OK      : {spread_allowed}")
            print(f"Session        : {session_name}")
            print(f"Session OK     : {session_allowed}")
            print(f"Reason         : {signal['reason']}")
            print(f"Strategy : {signal['strategy']}")
            print(f"Confidence : {signal['confidence']}%")
            print(f"Open Position  : {open_position}")
            print(f"Position Type  : {position_type}")
            if sl is None:

                print("Stop Loss      : --")
                print("Take Profit    : --")

            else:

                print(f"Stop Loss      : {sl}")
                print(f"Take Profit    : {tp}")
            if signal["signal"] == Signal.NO_TRADE:

                print("Lot Size       : --")

            else:

                print(f"Lot Size       : {lot}")
            print("-" * 70)
            print(f"Bullish Engulfing : {bullish_engulfing(df)}")
            print(f"Bearish Engulfing : {bearish_engulfing(df)}")
            print(f"Doji              : {doji(df)}")
            print(f"Pin Bar           : {pin_bar(df)}")

            # =====================================
            # SAVE SIGNAL
            # =====================================
            log_trade(
                SYMBOL,
                signal["trend"],
                signal["signal"].value,
                last["close"],
                sl,
                tp,
                lot,
                signal["reason"]
            )
            print("✅ Trade Logged Successfully")
            print("=" * 70)

            # =====================================
            # AUTO TRADING
            # =====================================
            if AUTO_TRADING:
                # ===============================
                # BUY SIGNAL
                # ===============================
                if (
                    signal["signal"] == Signal.BUY
                    and buy_allowed
                    and spread_allowed
                    and session_allowed
                    and lot > 0
                    and sl is not None
                    and tp is not None
                ):
                    if position_type == "BUY":
                        print("🟡 BUY Position Already Open")
                        print("Skipping Trade...")
                    else:
                        closed = True
                        if position_type == "SELL":
                            print("🔄 Closing SELL Position...")
                            print(execute_close())
                            closed = wait_until_position_closed()
                        if closed:
                            print("🟢 Opening BUY Position...")
                            result = execute_buy(lot, sl, tp)
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
                        else:
                            print("❌ Failed To Close SELL Position")

                # ===============================
                # SELL SIGNAL
                # ===============================
                elif (
                    signal["signal"] == Signal.SELL
                    and sell_allowed
                    and spread_allowed
                    and session_allowed
                    and lot > 0
                    and sl is not None
                    and tp is not None
                ):
                    if position_type == "SELL":
                        print("🟡 SELL Position Already Open")
                        print("Skipping Trade...")
                    else:
                        closed = True
                        if position_type == "BUY":
                            print("🔄 Closing BUY Position...")
                            print(execute_close())
                            closed = wait_until_position_closed()
                        if closed:
                            print("🔴 Opening SELL Position...")
                            result = execute_sell(lot, sl, tp)
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
                            print("❌ Failed To Close BUY Position")
            else:
                print("⚪ Auto Trading Disabled")

            # =====================================
            # BREAK EVEN
            # =====================================
            if open_position:
                be_result = move_to_break_even()
                if be_result is not None:
                    print()
                    print("🟢 Break Even Activated")
                    print(be_result)

            # =====================================
            # TRAILING STOP
            # =====================================
            if open_position:
                ts_result = trailing_stop(df)
                if ts_result is not None:
                    print()
                    print("🔵 Trailing Stop Updated")
                    print(ts_result)

            # =====================================
            # LOOP DELAY
            # =====================================
            time.sleep(1)

    # =====================================
    # USER STOP
    # =====================================
    except KeyboardInterrupt:
        print()
        print("🛑 Bot Stopped By User")

    # =====================================
    # UNKNOWN ERROR
    # =====================================
    except Exception as e:
        print()
        print("❌ Unexpected Error")
        print(e)

    # =====================================
    # CLOSE MT5
    # =====================================
    finally:
        mt5.shutdown()
        print("✅ MT5 Connection Closed")


# =====================================
# ENTRY POINT
# =====================================

if __name__ == "__main__":
    main()

            