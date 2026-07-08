import MetaTrader5 as mt5

from config import SYMBOL
from mt5.symbol_info import (
    get_symbol_info,
    get_point,
    get_digits,
    get_spread,
    get_min_lot,
    get_max_lot,
    get_lot_step,
    get_stop_level,
    get_tick_value,
    get_tick_size,
    get_filling_mode,
    get_execution_mode
)

print("=" * 70)
print("🚀 AI Trading Bot - System Test")
print("=" * 70)

# =====================================
# MT5 CONNECTION
# =====================================

if not mt5.initialize():

    print("❌ MT5 Connection Failed")
    print(mt5.last_error())
    quit()

print("✅ MT5 Connected")

account = mt5.account_info()

print(f"Broker     : {account.server}")
print(f"Company    : {account.company}")
print(f"Login      : {account.login}")
print(f"Balance    : {account.balance}")

print("-" * 70)

# =====================================
# SYMBOL
# =====================================

symbol = get_symbol_info()

print(f"Symbol         : {symbol.name}")
print(f"Digits         : {get_digits()}")
print(f"Point          : {get_point()}")
print(f"Spread         : {get_spread()}")
print(f"Min Lot        : {get_min_lot()}")
print(f"Max Lot        : {get_max_lot()}")
print(f"Lot Step       : {get_lot_step()}")
print(f"Stop Level     : {get_stop_level()}")
print(f"Tick Size      : {get_tick_size()}")
print(f"Tick Value     : {get_tick_value()}")
print(f"Execution Mode : {get_execution_mode()}")
print(f"Filling Mode   : {get_filling_mode()}")

print("-" * 70)

# =====================================
# TICK DATA
# =====================================

tick = mt5.symbol_info_tick(SYMBOL)

if tick is None:

    print("❌ Tick Data Failed")

else:

    print("✅ Tick Data OK")
    print(f"Bid : {tick.bid}")
    print(f"Ask : {tick.ask}")

print("-" * 70)

# =====================================
# ACCOUNT CHECK
# =====================================

print("Trade Allowed :", account.trade_allowed)
print("Expert Enabled:", account.trade_expert)

print("-" * 70)

# =====================================
# TERMINAL CHECK
# =====================================

terminal = mt5.terminal_info()

print("Terminal :", terminal.name)
print("Build    :", terminal.build)

print("=" * 70)

print("✅ SYSTEM TEST PASSED")

mt5.shutdown()