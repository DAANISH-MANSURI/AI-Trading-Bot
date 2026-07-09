"""
Chart Visualization Layer for AI Trading Bot
Phase 4: Draws FVG zones, S/R zones, BOS/CHOCH signals, and Fibonacci Golden Zone on MT5 charts.
"""
import MetaTrader5 as mt5
from mt5.mt5_connector import (
    _ensure_initialized,
    shutdown_mt5,
    chart_get_chart_id,
    chart_objects_delete_by_prefix,
    chart_create_rectangle,
    chart_create_arrow,
    chart_create_text,
)

# Object name prefix for our drawings
OBJECT_PREFIX = "AITB_"

# Colors (as integers in 0x00BBGGRR format)
CLR_GREEN = 0x008000
CLR_RED = 0xFF0000
CLR_BLUE = 0x0000FF
CLR_YELLOW = 0xFFFF00
CLR_ORANGE = 0xFFA500
CLR_WHITE = 0xFFFFFF
CLR_GRAY = 0x808080
CLR_BLACK = 0x000000

# Arrow codes from Wingdings font
ARROW_UP = 217
ARROW_DOWN = 218


def _get_chart_id(symbol: str, timeframe: int) -> int:
    """
    Get the chart ID for the given symbol and timeframe.
    Initializes MT5 if needed.
    Returns 0 if chart not found or initialization failed.
    """
    if not _ensure_initialized():
        return 0
    chart_id = chart_get_chart_id(symbol, timeframe)
    if chart_id == 0:
        print(f"⚠️ No chart found for {symbol} timeframe {timeframe}")
    return chart_id


def cleanup_chart_objects(symbol: str, timeframe: int) -> bool:
    """
    Remove all chart objects with our prefix for the given symbol and timeframe.
    """
    chart_id = _get_chart_id(symbol, timeframe)
    if chart_id == 0:
        return False
    result = chart_objects_delete_by_prefix(chart_id, OBJECT_PREFIX)
    # Shutdown MT5 after cleanup? We'll let the caller manage initialization/shutdown.
    # For now, we don't shutdown here because we might draw immediately after.
    return result


def draw_fvg_zones(symbol: str, timeframe: int, fvg_list: list) -> bool:
    """
    Draw FVG zones as rectangles.
    Bullish FVG: green rectangle
    Bearish FVG: red rectangle
    Each FVG in fvg_list should be a dict with:
        - 'direction': 'bullish' or 'bearish'
        - 'price_high': top of the FVG (float)
        - 'price_low': bottom of the FVG (float)
        - 'time_start': start time (float, MT5 time format)
        - 'time_end': end time (float, MT5 time format)
    """
    if not fvg_list:
        return True

    chart_id = _get_chart_id(symbol, timeframe)
    if chart_id == 0:
        return False

    success = True
    for i, fvg in enumerate(fvg_list):
        direction = fvg.get('direction', '').lower()
        price_high = fvg.get('price_high')
        price_low = fvg.get('price_low')
        time_start = fvg.get('time_start')
        time_end = fvg.get('time_end')

        if None in (direction, price_high, price_low, time_start, time_end):
            print(f"⚠️ Invalid FVG data at index {i}: {fvg}")
            success = False
            continue

        # Determine color
        if direction == 'bullish':
            color = CLR_GREEN
        elif direction == 'bearish':
            color = CLR_RED
        else:
            print(f"⚠️ Unknown FVG direction: {direction}")
            success = False
            continue

        # Create unique object name
        obj_name = f"{OBJECT_PREFIX}FVG_{direction}_{int(time_start)}_{i}"

        # Draw rectangle: from (time_start, price_low) to (time_end, price_high)
        if not chart_create_rectangle(
            chart_id,
            obj_name,
            time1=time_start,
            price1=price_low,
            time2=time_end,
            price2=price_high,
            color=color,
            width=1,
            style=0,  # solid line
            background_color=color,
            fill=True  # fill the rectangle
        ):
            success = False
            # Continue to draw other FVGs

    return success


def draw_sr_zones(symbol: str, timeframe: int, sr_zone_list: list) -> bool:
    """
    Draw S/R zones as rectangles with visual strength representation.
    Strength (score 0-100) is represented by rectangle border thickness.
    Higher score = thicker border.
    Each S/R zone in sr_zone_list should be a dict with:
        - 'price_high': top of the zone (float)
        - 'price_low': bottom of the zone (float)
        - 'time_start': start time (float)
        - 'time_end': end time (float)
        - 'score': strength score (0-100, int or float)
    """
    if not sr_zone_list:
        return True

    chart_id = _get_chart_id(symbol, timeframe)
    if chart_id == 0:
        return False

    success = True
    for i, zone in enumerate(sr_zone_list):
        price_high = zone.get('price_high')
        price_low = zone.get('price_low')
        time_start = zone.get('time_start')
        time_end = zone.get('time_end')
        score = zone.get('score', 50)  # default to middle strength

        if None in (price_high, price_low, time_start, time_end):
            print(f"⚠️ Invalid S/R zone data at index {i}: {zone}")
            success = False
            continue

        # Ensure score is within 0-100
        score = max(0, min(100, score))
        # Map score to line width: 1 (min) to 3 (max)
        width = int(1 + (score / 100) * 2)  # 1 to 3

        # Create unique object name
        obj_name = f"{OBJECT_PREFIX}SR_{int(time_start)}_{i}"

        # Draw rectangle: from (time_start, price_low) to (time_end, price_high)
        if not chart_create_rectangle(
            chart_id,
            obj_name,
            time1=time_start,
            price1=price_low,
            time2=time_end,
            price2=price_high,
            color=CLR_BLUE,
            width=width,
            style=0,
            background_color=CLR_BLUE,
            fill=False  # no fill, just border
        ):
            success = False

    return success


def draw_bos_choch(symbol: str, timeframe: int, events: list) -> bool:
    """
    Draw BOS and CHOCH events as arrows.
    Bullish BOS/CHOCH: up arrow
    Bearish BOS/CHOCH: down arrow
    BOS: solid color (green for bullish, red for bearish)
    CHOCH: different color (blue for bullish, orange for bearish) to distinguish
    Each event in events should be a dict with:
        - 'type': 'bos' or 'choch'
        - 'direction': 'bullish' or 'bearish'
        - 'time': break time (float)
        - 'price': break price (float)
    """
    if not events:
        return True

    chart_id = _get_chart_id(symbol, timeframe)
    if chart_id == 0:
        return False

    success = True
    for i, event in enumerate(events):
        event_type = event.get('type', '').lower()
        direction = event.get('direction', '').lower()
        time_val = event.get('time')
        price_val = event.get('price')

        if None in (event_type, direction, time_val, price_val):
            print(f"⚠️ Invalid BOS/CHOCH event data at index {i}: {event}")
            success = False
            continue

        # Determine arrow color and type
        if direction == 'bullish':
            if event_type == 'bos':
                color = CLR_GREEN
            elif event_type == 'choch':
                color = CLR_BLUE  # blue for bullish CHOCH
            else:
                print(f"⚠️ Unknown event type: {event_type}")
                success = False
                continue
            arrow_code = ARROW_UP
        elif direction == 'bearish':
            if event_type == 'bos':
                color = CLR_RED
            elif event_type == 'choch':
                color = CLR_ORANGE  # orange for bearish CHOCH
            else:
                print(f"⚠️ Unknown event type: {event_type}")
                success = False
                continue
            arrow_code = ARROW_DOWN
        else:
            print(f"⚠️ Unknown direction: {direction}")
            success = False
            continue

        # Create unique object name
        obj_name = f"{OBJECT_PREFIX}{event_type}_{direction}_{int(time_val)}_{i}"

        # Draw arrow at the break point
        if not chart_create_arrow(
            chart_id,
            obj_name,
            time1=time_val,
            price1=price_val,
            angle=0,
            arrow_code=arrow_code,
            color=color,
            width=2,
            style=0
        ):
            success = False

    return success


def draw_fibonacci_golden_zone(symbol: str, timeframe: int, swing_data: dict) -> bool:
    """
    Draw Fibonacci Golden Zone (50%-61.8%) as a rectangle.
    The golden zone is the area between the 50% and 61.8% retracement levels
    from the swing start (point1) to swing end (point2).
    swing_data should be a dict with:
        - 'time1': time of swing start (float)
        - 'price1': price of swing start (float)
        - 'time2': time of swing end (float)
        - 'price2': price of swing end (float)
    The rectangle will be drawn from (time1 from point1 and point2 at 50% and 61.8%),
        to time2, max(y from point1 and point2 at 50% and 61.8%).
    """
    if not swing_data:
        return True

    time1 = swing_data.get('time1')
    price1 = swing_data.get('price1')
    time2 = swing_data.get('time2')
    price2 = swing_data.get('price2')

    if None in (time1, price1, time2, price2):
        print(f"⚠️ Invalid swing data for Fibonacci: {swing_data}")
        return False

    # Calculate the 50% and 61.8% price levels
    price_diff = price2 - price1
    y50 = price1 + 0.5 * price_diff
    y61 = price1 + 0.618 * price_diff

    # Determine the bottom and top of the golden zone rectangle
    zone_bottom = min(y50, y61)
    zone_top = max(y50, y61)

    # Create unique object name
    obj_name = f"{OBJECT_PREFIX}FIBO_GZ_{int(time1)}_{int(time2)}"

    chart_id = _get_chart_id(symbol, timeframe)
    if chart_id == 0:
        return False

    # Draw rectangle representing the golden zone
    return chart_create_rectangle(
        chart_id,
        obj_name,
        time1=time1,
        price1=zone_bottom,
        time2=time2,
        price2=zone_top,
        color=CLR_YELLOW,
        width=1,
        style=0,  # solid line
        background_color=CLR_YELLOW,
        fill=True  # fill the rectangle with yellow
    )


def draw_all_chart_objects(symbol: str, timeframe: int, data: dict) -> bool:
    """
    Main function to draw all chart objects.
    First cleans up existing objects with our prefix, then draws new ones.
    data dict should contain:
        - 'fvg': list of FVG dicts (see draw_fvg_zones)
        - 'sr_zones': list of S/R zone dicts (see draw_sr_zones)
        - 'bos_choch': list of BOS/CHOCH event dicts (see draw_bos_choch)
        - 'fibonacci': swing data dict (see draw_fibonacci_golden_zone)
    """
    # Cleanup existing drawings
    if not cleanup_chart_objects(symbol, timeframe):
        print("⚠️ Cleanup failed, but continuing to draw")

    # Draw each type
    success = True
    success = draw_fvg_zones(symbol, timeframe, data.get('fvg', [])) and success
    success = draw_sr_zones(symbol, timeframe, data.get('sr_zones', [])) and success
    success = draw_bos_choch(symbol, timeframe, data.get('bos_choch', [])) and success
    success = draw_fibonacci_golden_zone(symbol, timeframe, data.get('fibonacci', {})) and success

    # Shutdown MT5 connection after drawing
    shutdown_mt5()
    return success


# Example usage (for testing)
if __name__ == "__main__":
    # This is just for demonstration; actual data would come from the strategy engine
    print("Chart Drawer Module - Example Usage")
    print("To use, call draw_all_chart_objects(symbol, timeframe, data)")
    #
    # Example data structure:
    # data = {
    #     'fvg': [
    #         {'direction': 'bullish', 'price_high': 1.1000, 'price_low': 1.0950, 'time_start': 1640995200, 'time_end': 1641081600},
    #     ],
    #     'sr_zones': [
    #         {'price_high': 1.1050, 'price_low': 1.1000, 'time_start': 1640995200, 'time_end': 1641081600, 'score': 80},
    #     ],
    #     'bos_choch': [
    #         {'type': 'bos', 'direction': 'bullish', 'time': 1641000000, 'price': 1.1025},
    #     ],
    #     'fibonacci': {
    #         'time1': 1640908800,  # swing start time
    #         'price1': 1.0900,     # swing start price
    #         'time2': 1641081600,  # swing end time
    #         'price2': 1.1100,     # swing end price
    #     }
    # }