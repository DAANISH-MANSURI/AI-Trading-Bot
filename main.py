"""
AI Trading Bot

Project Launcher
"""

from backtesting.backtest import main as run_backtest


def menu():

    print("=" * 60)
    print("AI Trading Bot")
    print("=" * 60)
    print("1. Backtesting")
    print("2. Live Trading (Coming Soon)")
    print("3. Optimizer (Coming Soon)")
    print("=" * 60)

    choice = input("Select Option : ")

    if choice == "1":
        run_backtest()

    elif choice == "2":
        print("Live Trading Module")

    elif choice == "3":
        print("Optimizer Module")

    else:
        print("Invalid Option")


if __name__ == "__main__":
    menu()