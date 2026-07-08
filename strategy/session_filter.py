from datetime import datetime
from zoneinfo import ZoneInfo


def london_session():

    now = datetime.now(ZoneInfo("UTC"))

    hour = now.hour

    return 8 <= hour < 17


def newyork_session():

    now = datetime.now(ZoneInfo("UTC"))

    hour = now.hour

    return 13 <= hour < 22


def trading_session():

    return london_session() or newyork_session()


def current_session():

    if london_session():
        return "LONDON"

    if newyork_session():
        return "NEW YORK"

    return "CLOSED"