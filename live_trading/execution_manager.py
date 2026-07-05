import time
import MetaTrader5 as mt5

from trade_executor import buy, sell
from close_position import close_position
from retcode_manager import get_retcode_message


# ==========================================
# BUY EXECUTION
# ==========================================

def execute_buy(lot, sl, tp, retries=3):

    for attempt in range(retries):

        print(f"\n🟢 BUY Attempt {attempt + 1}")

        result = buy(
            lot,
            sl,
            tp
        )

        if result is None:

            time.sleep(1)
            continue

        if result.retcode == mt5.TRADE_RETCODE_DONE:

            print("✅ BUY Executed Successfully")

            return result

        print(get_retcode_message(result.retcode))

        time.sleep(1)

    print("❌ BUY Failed")

    return None


# ==========================================
# SELL EXECUTION
# ==========================================

def execute_sell(lot, sl, tp, retries=3):

    for attempt in range(retries):

        print(f"\n🔴 SELL Attempt {attempt + 1}")

        result = sell(
            lot,
            sl,
            tp
        )

        if result is None:

            time.sleep(1)
            continue

        if result.retcode == mt5.TRADE_RETCODE_DONE:

            print("✅ SELL Executed Successfully")

            return result

        print(get_retcode_message(result.retcode))

        time.sleep(1)

    print("❌ SELL Failed")

    return None


# ==========================================
# CLOSE POSITION
# ==========================================

def execute_close(retries=3):

    for attempt in range(retries):

        print(f"\n🟡 CLOSE Attempt {attempt + 1}")

        result = close_position()

        if result is None:

            time.sleep(1)
            continue

        if result.retcode == mt5.TRADE_RETCODE_DONE:

            print("✅ Position Closed Successfully")

            return result

        print(get_retcode_message(result.retcode))

        time.sleep(1)

    print("❌ Close Position Failed")

    return None