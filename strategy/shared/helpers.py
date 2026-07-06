"""
Common Helper Functions
"""

import math


def round_price(price, digits=2):
    """
    Round price safely.
    """
    return round(price, digits)


def percentage_difference(value1, value2):
    """
    Percentage difference between two values.
    """

    if value2 == 0:
        return 0

    return abs(value1 - value2) / value2 * 100


def within_tolerance(price, reference, tolerance):

    """
    Check whether price lies within
    tolerance distance.
    """

    return abs(price - reference) <= tolerance


def clamp(value, minimum, maximum):

    """
    Clamp value between min and max.
    """

    return max(minimum, min(value, maximum))