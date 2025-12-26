import pytz
import time

from datetime import datetime
from dateutil import parser


def get_current_local_utc_time() -> datetime:
    local_now = datetime.now(pytz.timezone(time.tzname[0]))
    return local_now.astimezone(pytz.timezone("UTC"))


def convert_time_to_utc(time: str) -> datetime:
    parsed_time = parser.parse(time)
    return parsed_time.astimezone(pytz.timezone("UTC"))
