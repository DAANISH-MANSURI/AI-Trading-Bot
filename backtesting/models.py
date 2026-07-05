from dataclasses import dataclass, field
from typing import Dict, List
import pandas as pd


@dataclass
class BacktestResult:
    """
    Stores complete backtest results.
    """

    symbol: str
    timeframe: str

    starting_balance: float
    final_balance: float

    trades: pd.DataFrame

    performance: Dict
    analytics: Dict
    drawdown: Dict

    equity_curve: List[float] = field(default_factory=list)

    report_path: str = ""
    csv_path: str = ""
    chart_path: str = ""

    def total_trades(self):

        return len(self.trades)

    def wins(self):

        if self.trades.empty:
            return 0

        return len(
            self.trades[
                self.trades["result"] == "WIN"
            ]
        )

    def losses(self):

        if self.trades.empty:
            return 0

        return len(
            self.trades[
                self.trades["result"] == "LOSS"
            ]
        )

    def net_profit(self):

        return round(
            self.final_balance -
            self.starting_balance,
            2
        )

    def return_percent(self):

        return round(

            (
                self.final_balance -
                self.starting_balance
            )

            / self.starting_balance * 100,

            2

        )

    def summary(self):

        return {

            "Symbol": self.symbol,

            "Timeframe": self.timeframe,

            "Starting Balance": self.starting_balance,

            "Final Balance": self.final_balance,

            "Net Profit": self.net_profit(),

            "Return %": self.return_percent(),

            "Trades": self.total_trades(),

            "Wins": self.wins(),

            "Losses": self.losses()

        }
@dataclass
class TradeResult:
    """
    Represents one completed trade.
    """

    signal: str

    result: str

    entry_time: object

    exit_time: object

    entry_price: float

    exit_price: float

    sl: float

    tp: float

    lot_size: float

    profit: float

    balance: float

    risk_amount: float

    rr: float

    trade_duration: int

    exit_reason: str

    exit_index: int

    def is_win(self):

        return self.result == "WIN"

    def is_loss(self):

        return self.result == "LOSS"

    def to_dict(self):

        return {

            "signal": self.signal,

            "result": self.result,

            "entry_time": self.entry_time,

            "exit_time": self.exit_time,

            "entry_price": self.entry_price,

            "exit_price": self.exit_price,

            "sl": self.sl,

            "tp": self.tp,

            "lot_size": self.lot_size,

            "profit": self.profit,

            "balance": self.balance,

            "risk_amount": self.risk_amount,

            "rr": self.rr,

            "trade_duration": self.trade_duration,

            "exit_reason": self.exit_reason,

            "exit_index": self.exit_index

        }