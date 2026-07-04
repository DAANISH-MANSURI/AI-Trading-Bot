import MetaTrader5 as mt5
from config import SYMBOL

if not mt5.initialize():
    print("❌ MT5 Connection Failed")
    quit()

symbol = mt5.symbol_info(SYMBOL)

if symbol is None:
    print(f"❌ {SYMBOL} Not Found")
    mt5.shutdown()
    quit()

print("=" * 60)
print("BROKER TEST")
print("=" * 60)

print("Broker        :", mt5.account_info().server)
print("Company       :", mt5.account_info().company)

print("Symbol        :", symbol.name)
print("Digits        :", symbol.digits)
print("Spread        :", symbol.spread)
print("Min Lot       :", symbol.volume_min)
print("Max Lot       :", symbol.volume_max)
print("Lot Step      :", symbol.volume_step)

print("Stops Level   :", symbol.trade_stops_level)
print("Freeze Level  :", symbol.trade_freeze_level)

print("Trade Mode    :", symbol.trade_mode)
print("Execution     :", symbol.trade_exemode)
print("Filling Mode  :", symbol.filling_mode)

mt5.shutdown()