import csv
import os
from datetime import datetime


LOG_FILE = "trade_log.csv"


def create_log_file():

    if not os.path.exists(LOG_FILE):

        with open(LOG_FILE, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Date",
                "Time",
                "Symbol",
                "Trend",
                "Signal",
                "Price",
                "Stop Loss",
                "Take Profit",
                "Lot Size",
                "Reason"
            ])


def log_trade(symbol,
              trend,
              signal,
              price,
              sl,
              tp,
              lot,
              reason):

    create_log_file()

    now = datetime.now()

    with open(LOG_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            symbol,
            trend,
            signal,
            price,
            sl,
            tp,
            lot,
            reason
        ])