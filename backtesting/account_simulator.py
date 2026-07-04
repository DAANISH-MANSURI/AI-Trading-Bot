class AccountSimulator:

    def __init__(
        self,
        starting_balance=10000,
        risk_percent=1
    ):

        self.starting_balance = starting_balance
        self.balance = starting_balance
        self.risk_percent = risk_percent

        self.trade_history = []

    # ==========================================
    # Current Balance
    # ==========================================

    def get_balance(self):

        return round(self.balance, 2)

    # ==========================================
    # Current Risk Amount
    # ==========================================

    def get_risk_amount(self):

        return self.balance * (self.risk_percent / 100)

    # ==========================================
    # Apply Trade Result
    # ==========================================

    def process_trade(self, trade):

        risk_amount = self.get_risk_amount()

        # WIN
        if trade["result"] == "WIN":

            profit = risk_amount * trade["rr"]

        # LOSS
        else:

            profit = -risk_amount

        self.balance += profit

        record = {

            "balance": round(self.balance, 2),

            "profit": round(profit, 2),

            "risk_amount": round(risk_amount, 2)

        }

        self.trade_history.append(record)

        return record