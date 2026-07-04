import os
import matplotlib.pyplot as plt


def generate_equity_curve(trades_df):

    if trades_df.empty:
        return

    os.makedirs("reports", exist_ok=True)

    plt.figure(figsize=(12, 6))

    plt.plot(
        trades_df["balance"],
        linewidth=2,
        label="Equity"
    )

    plt.title("AI Trading Bot - Equity Curve")

    plt.xlabel("Trade Number")

    plt.ylabel("Account Balance ($)")

    plt.grid(True)

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "reports/equity_curve.png",
        dpi=300
    )

    plt.close()