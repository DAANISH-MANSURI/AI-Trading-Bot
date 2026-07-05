import MetaTrader5 as mt5


def get_retcode_message(retcode):

    codes = {

        mt5.TRADE_RETCODE_DONE:
            "✅ Trade Executed Successfully",

        mt5.TRADE_RETCODE_REQUOTE:
            "⚠️ Requote",

        mt5.TRADE_RETCODE_REJECT:
            "❌ Order Rejected",

        mt5.TRADE_RETCODE_CANCEL:
            "❌ Order Cancelled",

        mt5.TRADE_RETCODE_PLACED:
            "🟢 Order Placed",

        mt5.TRADE_RETCODE_DONE_PARTIAL:
            "⚠️ Partially Filled",

        mt5.TRADE_RETCODE_ERROR:
            "❌ Trade Error",

        mt5.TRADE_RETCODE_TIMEOUT:
            "⌛ Request Timeout",

        mt5.TRADE_RETCODE_INVALID:
            "❌ Invalid Request",

        mt5.TRADE_RETCODE_INVALID_VOLUME:
            "❌ Invalid Volume",

        mt5.TRADE_RETCODE_INVALID_PRICE:
            "❌ Invalid Price",

        mt5.TRADE_RETCODE_INVALID_STOPS:
            "❌ Invalid Stop Loss / Take Profit",

        mt5.TRADE_RETCODE_TRADE_DISABLED:
            "❌ Trading Disabled",

        mt5.TRADE_RETCODE_MARKET_CLOSED:
            "🛑 Market Closed",

        mt5.TRADE_RETCODE_NO_MONEY:
            "❌ Not Enough Margin",

        mt5.TRADE_RETCODE_PRICE_CHANGED:
            "⚠️ Price Changed",

        mt5.TRADE_RETCODE_PRICE_OFF:
            "⚠️ No Prices",

        mt5.TRADE_RETCODE_INVALID_FILL:
            "❌ Unsupported Filling Mode",

        mt5.TRADE_RETCODE_CONNECTION:
            "❌ Connection Lost"

    }

    return codes.get(retcode, f"Unknown Error ({retcode})")