import MetaTrader5 as mt5

if not mt5.initialize():
    print("MT5 Connection Failed")
    quit()

symbols = mt5.symbols_get()

print("=" * 60)
print("Available BTC Symbols")
print("=" * 60)

for s in symbols:
    if "BTC" in s.name.upper():
        print(s.name)

mt5.shutdown()