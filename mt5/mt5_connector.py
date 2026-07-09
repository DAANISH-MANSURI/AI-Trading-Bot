import MetaTrader5 as mt5
from typing import Optional

# Define color constants for MT5 objects (in 0x00BBGGRR format)
# These are the actual integer values used by the MT5 Python package for colors
clr_red = 0x0000FF      # Red
clr_blue = 0xFF0000     # Blue
clr_green = 0x008000    # Green
clr_none = 0xFFFFFFFF   # No color (for transparent background)


def connect_mt5():
    """
    Original function: initializes MT5, prints account info, and shuts down.
    Kept for backward compatibility.
    """
    if not mt5.initialize():
        print("❌ MT5 Initialization Failed")
        print(mt5.last_error())
        return False

    account = mt5.account_info()

    if account is None:
        print("❌ MT5 Login Required")
        mt5.shutdown()
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
    return True


def _ensure_initialized() -> bool:
    """
    Initialize MT5 connection if not already initialized.
    Returns True if successful, False otherwise.
    """
    if not mt5.terminal_info():
        # Not initialized
        if not mt5.initialize():
            print("❌ MT5 Initialization Failed")
            print(mt5.last_error())
            return False
    return True


def shutdown_mt5():
    """
    Shutdown the MT5 connection if it was initialized.
    """
    if mt5.terminal_info():
        mt5.shutdown()


def chart_get_chart_id(symbol: str, timeframe: int) -> int:
    """
    Find the chart ID for the given symbol and timeframe.
    Returns 0 if not found.
    """
    if not _ensure_initialized():
        return 0

    chart_id = mt5.chart_first()
    while chart_id != 0:
        if (mt5.symbol_get_string(chart_id, mt5.SYMBOL_NAME) == symbol and
                mt5.chart_get_integer(chart_id, mt5.CHART_PERIOD) == timeframe):
            return chart_id
        chart_id = mt5.chart_next(chart_id)
    return 0


def chart_object_create(chart_id: int, name: str, obj_type: int, time1: float, price1: float,
                        time2: float = 0, price2: float = 0, time3: float = 0, price3: float = 0,
                        **kwargs) -> bool:
    """
    Create a chart object.
    Wrapper around mt5.object_create with error handling.
    """
    if not _ensure_initialized():
        return False
    if chart_id == 0:
        print("❌ Invalid chart ID")
        return False

    result = mt5.object_create(chart_id, name, obj_type, time1, price1, time2, price2, time3, price3, **kwargs)
    if not result:
        print(f"❌ Failed to create object '{name}': {mt5.last_error()}")
    return result


def chart_object_delete(chart_id: int, name: str) -> bool:
    """
    Delete a chart object by name.
    """
    if not _ensure_initialized():
        return False
    if chart_id == 0:
        print("❌ Invalid chart ID")
        return False

    result = mt5.object_delete(chart_id, name)
    if not result:
        print(f"❌ Failed to delete object '{name}': {mt5.last_error()}")
    return result


def chart_objects_delete_by_prefix(chart_id: int, prefix: str) -> bool:
    """
    Delete all chart objects whose name starts with the given prefix.
    Returns True if at least one operation succeeded or if no objects found.
    Returns False if there was an error.
    """
    if not _ensure_initialized():
        return False
    if chart_id == 0:
        print("❌ Invalid chart ID")
        return False

    total = mt5.objects_total(chart_id)
    if total == 0:
        return True  # nothing to delete

    success = False
    # We need to iterate from the last to first because deleting changes indices
    for i in range(total - 1, -1, -1):
        name = mt5.object_name(chart_id, i)
        if name.startswith(prefix):
            if mt5.object_delete(chart_id, name):
                success = True
            else:
                print(f"❌ Failed to delete object '{name}': {mt5.last_error()}")
    return success


# Convenience functions for specific object types
def chart_create_rectangle(chart_id: int, name: str, x1: float, y1: float, x2: float, y2: float,
                           color: int = clr_red, width: int = 1, style: int = 0,
                           background_color: int = clr_none, fill: bool = False, z_order: int = 0) -> bool:
    """
    Create a rectangle object.
    OBJ_RECTANGLE = 0
    """
    return chart_object_create(
        chart_id, name, mt5.OBJ_RECTANGLE,
        x1, y1, x2, y2,
        color=color, width=width, style=style,
        background_color=background_color, fill=fill, z_order=z_order
    )


def chart_create_arrow(chart_id: int, name: str, time1: float, price1: float,
                       angle: int = 0, arrow_code: int = 217, color: int = clr_red,
                       width: int = 1, style: int = 0, z_order: int = 0) -> bool:
    """
    Create an arrow object.
    OBJ_ARROW = 2
    """
    return chart_object_create(
        chart_id, name, mt5.OBJ_ARROW,
        time1, price1, 0, 0, 0, 0,
        angle=angle, arrow_code=arrow_code, color=color,
        width=width, style=style, z_order=z_order
    )


def chart_create_text(chart_id: int, name: str, time1: float, price1: float,
                      text: str, font: str = "Arial", font_size: int = 10,
                      color: int = clr_red, anchor: int = 0, x_offset: int = 0, y_offset: int = 0,
                      z_order: int = 0) -> bool:
    """
    Create a text object.
    OBJ_TEXT = 0
    """
    return chart_object_create(
        chart_id, name, mt5.OBJ_TEXT,
        time1, price1, 0, 0, 0, 0,
        text=text, font=font, font_size=font_size,
        color=color, anchor=anchor, x_offset=x_offset, y_offset=y_offset,
        z_order=z_order
    )


def chart_create_fibo(chart_id: int, name: str, time1: float, price1: float,
                      time2: float, price2: float,
                      color: int = clr_blue, width: int = 1, style: int = 0) -> bool:
    """
    Create a Fibonacci object.
    OBJ_FIBO = 32
    Note: After creation, you may need to set the Fibonacci levels using object_set functions.
    """
    return chart_object_create(
        chart_id, name, mt5.OBJ_FIBO,
        time1, price1, time2, price2, 0, 0,
        color=color, width=width, style=style
    )