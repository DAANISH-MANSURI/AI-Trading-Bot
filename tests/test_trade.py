import MetaTrader5 as mt5
from trade_executor import buy

if not mt5.initialize():
    print("❌ MT5 Connection Failed")
    quit()

print("=" * 60)
print("Sending BUY Order...")
print("=" * 60)

result = buy(
    symbol="EURUSD",
    lot=0.01,
    sl_points=300,
    tp_points=600
)

if result is None:
    print("❌ Order returned None")

else:
    print("\nResult Object")
    print(result)

    print("\nRetcode :", result.retcode)
    print("Comment :", result.comment)
    print("Order   :", result.order)
    print("Deal    :", result.deal)

mt5.shutdown()