import MetaTrader5 as mt5


def connect_mt5():
    if not mt5.initialize():
        print("❌ MT5 Initialization Failed")
        print(mt5.last_error())
        return False

    account = mt5.account_info()

    if account is None:
        print("❌ MT5 Login Required")
        return False

    print("=" * 40)
    print("✅ MT5 Connected Successfully")
    print("=" * 40)

    print(f"Login      : {account.login}")
    print(f"Server     : {account.server}")
    print(f"Name       : {account.name}")
    print(f"Balance    : {account.balance}")
    print(f"Equity     : {account.equity}")
    print(f"Leverage   : {account.leverage}")
    print(f"Currency   : {account.currency}")

    mt5.shutdown()


if __name__ == "__main__":
    connect_mt5()