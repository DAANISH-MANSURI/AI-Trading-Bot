import MetaTrader5 as mt5

if not mt5.initialize():
    print("❌ MT5 Connection Failed")
    quit()

account = mt5.account_info()
symbol = mt5.symbol_info("XAUUSD")
tick = mt5.symbol_info_tick("XAUUSD")

print("=" * 60)
print("ACCOUNT")
print("=" * 60)
print(account)

print("\n" + "=" * 60)
print("SYMBOL")
print("=" * 60)
print(symbol)

print("\n" + "=" * 60)
print("TICK")
print("=" * 60)
print(tick)

mt5.shutdown()