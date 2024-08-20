import locale
import os
import time
from datetime import datetime, timezone
from typing import Literal, Union

from rich.status import Status

__all__ = [
    "countdown_timer",
    "timestamp_to_readable",
    "timestamp_to_concise",
    "timestamp_to_locale",
    "filename_timestamp",
]


def countdown_timer(
    status: Status, duration: int, current_count: int, overall_count: int
):
    """
    Handles the live countdown during pagination, updating the status bar with the remaining time.

    :param status: The rich.status.Status object used to display the countdown.
    :type status: rich.status.Status
    :param duration: The duration for which to run the countdown.
    :type duration: int
    :param current_count: Current number of items fetched.
    :type current_count: int
    :param overall_count: Overall number of items to fetch.
    :type overall_count: int
    """
    end_time: float = time.time() + duration
    while time.time() < end_time:
        remaining_time: float = end_time - time.time()
        remaining_seconds: int = int(remaining_time)
        remaining_milliseconds: int = int((remaining_time - remaining_seconds) * 100)

        status.update(
            f"Fetched [cyan]{current_count}[/]/[cyan]{overall_count}[/] items so far. "
            f"Resuming in [cyan]{remaining_seconds}[/].[cyan]{remaining_milliseconds:02}[/]ms..."
        )
        time.sleep(0.01)  # Sleep for 10 milliseconds


def timestamp_to_locale(timestamp: float) -> str:
    """
    Converts a unix timestamp to a localized datetime string based on the system's locale.

    :param timestamp: Unix timestamp to convert.
    :type timestamp: float
    :return: A localized datetime string from the converted timestamp.
    :rtype: str

    Usage::

        >>> from knewkarma.tools.time_utils import timestamp_to_locale

        >>> coffee_time = 1722277062
        >>> difference = timestamp_to_locale(timestamp=coffee_time)
        >>> print(f"Coffee time was at {difference}")

        # As of writing :)
        Coffee time was at 29/07/24, 20:17:42
    """
    # Set the locale to the user's system default
    locale.setlocale(locale.LC_TIME, "")

    # Convert timestamp to a timezone-aware datetime object in UTC
    utc_object = datetime.fromtimestamp(timestamp, timezone.utc)

    local_object = utc_object.astimezone()

    # Format the datetime object according to the locale's conventions
    return local_object.strftime("%x, %X")


def timestamp_to_concise(timestamp: int) -> str:
    """
    Convert a Unix timestamp into a human-readable concise time difference.

    :param timestamp: A Unix timestamp.
    :type timestamp: int
    :return: A string representing the time difference from now.
    :rtype: str

    Usage::

        >>> from knewkarma.tools.time_utils import timestamp_to_concise

        >>> coffee_time = 1722277062
        >>> difference = timestamp_to_concise(timestamp=coffee_time)
        >>> print(f"Coffee time was {difference} ago")

        # As of writing :)
        Coffee time was 10 minutes ago
    """

    # Convert the current time to a Unix timestamp
    now = int(time.time())

    # Calculate the difference in seconds
    diff = now - timestamp

    # Define the time thresholds in seconds
    minute = 60
    hour = 60 * minute
    day = 24 * hour
    week = 7 * day
    month = 30 * day
    year = 12 * month

    # Determine the time unit and value
    if diff < minute:
        count = diff
        label = "seconds" if int(count) > 1 else "second"  # seconds
    elif diff < hour:
        count = diff // minute
        label = "minutes" if int(count) > 1 else "minute"  # minutes
    elif diff < day:
        count = diff // hour
        label = "hours" if int(count) > 1 else "hour"  # hours
    elif diff < week:
        count = diff // day
        label = "days" if int(count) > 1 else "day"
    elif diff < month:
        count = diff // week
        label = "weeks" if int(count) > 1 else "week"
    elif diff < year:
        count = diff // month
        label = "months" if int(count) > 1 else "month"
    else:
        count = diff // year
        label = "years" if int(count) > 1 else "year"

    return "just now" if int(count) == 0 else f"{int(count)} {label}"


def timestamp_to_readable(
    timestamp: float, time_format: Literal["concise", "locale"] = "locale"
) -> Union[str, None]:
    """
    Converts a Unix timestamp into a more readable format based on the specified `time_format`.
    The function supports converting the timestamp into either a localized datetime string or a concise
    human-readable time difference (e.g., "3 hours ago").

    :param timestamp: The Unix timestamp to be converted.
    :type timestamp: float
    :param time_format: Determines the format of the output time. Use "concise" for a human-readable
                        time difference, or "locale" for a localized datetime string. Defaults to "locale".
    :type time_format: Literal["concise", "locale"]
    :return: A string representing the formatted time. The format is determined by the `time_format` parameter.
    :rtype: str
    :raises ValueError: If `time_format` is not one of the expected values ("concise" or "locale").

    Usage::

        >>> from knewkarma.tools.time_utils import timestamp_to_readable

        >>> coffee_time = 1722277062
        >>> difference = timestamp_to_readable(timestamp=coffee_time, time_format="concise")
        >>> print(f"Coffee time was {difference} ago")

        # As of writing :)
        Coffee time was 10 minutes ago
    """
    if timestamp and isinstance(timestamp, float):
        if time_format == "concise":
            concise_time: str = timestamp_to_concise(timestamp=int(timestamp))
            return f"{concise_time} ago"
        elif time_format == "locale":
            return timestamp_to_locale(timestamp=timestamp)
        else:
            raise ValueError(
                f"Unknown time format {time_format}. Expected `concise` or `locale`."
            )
    else:
        return None


def filename_timestamp() -> str:
    """
    Generates a timestamp string suitable for file naming, based on the current date and time.
    The format of the timestamp is adapted based on the operating system.

    :return: The formatted timestamp as a string. The format is "%d-%B-%Y-%I-%M-%S%p" for Windows
             and "%d-%B-%Y-%I:%M:%S%p" for non-Windows systems.
    :rtype: str

    Example
    -------
    - Windows: "20-July-1969-08-17-45PM"
    - Non-Windows: "20-July-1969-08:17:45PM"
    """
    now = datetime.now()
    return (
        now.strftime("%d-%B-%Y-%I-%M-%S%p")
        if os.name == "nt"
        else now.strftime("%d-%B-%Y-%I:%M:%S%p")
    )


# -------------------------------- END ----------------------------------------- #
