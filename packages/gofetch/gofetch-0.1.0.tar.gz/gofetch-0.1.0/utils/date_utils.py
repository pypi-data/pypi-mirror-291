"Date utility functions"

from datetime import datetime

import pytz


def convert_to_iso(date: str = None) -> datetime:
    """
    Converts a date string to a timezone-aware datetime object in UTC.
    If no date is provided, returns None.

    @params:
    - date (str):
        The date string in ISO format.

    @returns:
    - datetime:
        The date converted to a timezone-aware datetime object in UTC.
    """
    if date:
        # Convert the string to a datetime object
        dt = datetime.fromisoformat(date)

        # Convert to UTC if it is not already timezone aware
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=pytz.UTC)
        else:
            dt = dt.astimezone(pytz.UTC)
    else:
        dt = None

    return dt
