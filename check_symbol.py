import MetaTrader5 as mt5

if not mt5.initialize():
    print("MT5 Connection Failed")
    quit()

symbol = mt5.symbol_info("XAUUSD")

print(symbol)
print("Stops Level :", symbol.trade_stops_level)
print("Freeze Level:", symbol.trade_freeze_level)

mt5.shutdown()