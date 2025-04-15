from jwt import encode
from random import choices
from string import digits, ascii_letters
from datetime import datetime, timezone, timedelta
from json import JSONDecodeError

from .constants import SIG_GEN_API, SIG_GEN_TOKEN
from .exceptions import RemoteGeneratorError, GeneratorServiceUnavailable
from . import log

from requests import get

def generate_x_signature(time: int, token: str | None = None) -> str:
    result = get(f"{SIG_GEN_API}/x-sig/generate?token={token or SIG_GEN_TOKEN}&time={str(time)}")
    log.debug(f"[SIG-GEN][{SIG_GEN_API}/x-sig/generate?token={token or SIG_GEN_TOKEN}&time={str(time)}]: {result.status_code}")
    if result.status_code == 200:
        data: dict = result.json()
        return data["sig"]
    try:
        data: dict = result.json()
        raise RemoteGeneratorError(data["error"])
    except JSONDecodeError:
        raise GeneratorServiceUnavailable(f"Service not found or unavailable")





def random_ascii_string(length=11) -> str:
    """
    Generates a random ASCII string.

    Args:
        length (int): Length of the generated string. Default is 11.

    Returns:
        str: Randomly generated ASCII string.
    """
    return ''.join(choices(digits+ascii_letters, k=length))


def get_utc_time() -> str:
    """
    Returns the current UTC time in ISO 8601 format.

    Returns:
        str: Current time in UTC with millisecond precision and 'Z' suffix.
    """
    return datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')

def get_target_date(days_from_now: int) -> str:
    """
    Returns the date after a specified number of days.

    Args:
        days_from_now (int): Number of days from the current date.

    Returns:
        str: Target date in "Day Mon DD YYYY HH:MM:SS GMT+0200" format.
    """
    target = datetime.now() + timedelta(days=days_from_now)
    return target.strftime('%a %b %d %Y %H:%M:%S GMT+0200')



def date_string_to_timestamp_ms(date: str) -> int:
    """
    Converts a date string in the format "DD.MM.YYYY" to a Unix timestamp in milliseconds.

    Args:
        date (str): The date string in the format "day.month.year" (e.g., "12.04.2003").

    Returns:
        int: The corresponding Unix timestamp in milliseconds since 01.01.1970 UTC.
    """
    dt = datetime.strptime(date, "%d.%m.%Y")
    return int(dt.timestamp() * 1000)