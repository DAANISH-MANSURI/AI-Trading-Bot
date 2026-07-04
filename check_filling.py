import MetaTrader5 as mt5

if not mt5.initialize():
    print("Connection Failed")
    quit()

symbol = mt5.symbol_info("EURUSD")

print("Filling Mode :", symbol.filling_mode)

mt5.shutdown()