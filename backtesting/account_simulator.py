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

        return round(

            self.balance * (self.risk_percent / 100),

            2

        )

    # ==========================================
    # Process TradeResult Object
    # ==========================================

    def process_trade(self, trade):

        """
        trade = TradeResult Object
        """

        risk_amount = self.get_risk_amount()

        # --------------------------------------
        # WIN
        # --------------------------------------

        if trade.is_win():

            profit = risk_amount * trade.rr

        # --------------------------------------
        # LOSS
        # --------------------------------------

        elif trade.is_loss():

            profit = -risk_amount

        else:

            raise ValueError(
                f"Unknown Trade Result : {trade.result}"
            )

        self.balance += profit

        self.balance = round(self.balance, 2)

        # --------------------------------------
        # Update Trade Object
        # --------------------------------------

        trade.profit = round(profit, 2)

        trade.balance = self.balance

        trade.risk_amount = risk_amount

        # --------------------------------------
        # Save History
        # --------------------------------------

        self.trade_history.append(trade)

        return trade