"""
This file is responsible for some utility functions, which help process data in some niche cases.
"""

from datetime import datetime, timedelta
from typing import Union, Tuple
from .record import Record


BD_INTERVAL = 7


def get_congrats_date(record_bd_now: datetime) -> Tuple:
    result = record_bd_now
    if record_bd_now.weekday() == 5:
        result = record_bd_now + timedelta(days=2)
    if record_bd_now.weekday() == 6:
        result = record_bd_now + timedelta(days=1)
    return result, record_bd_now


def is_bd_in_range(record: Record, delta: Union[int, None]) -> Union[datetime, None]:
    today = datetime.today()
    if record.birthday is None: return None
    record_bd_now = record.birthday.bd_date.replace(year=today.year)
    if record_bd_now < today or record_bd_now > (today + timedelta(days=BD_INTERVAL if delta is None else delta)):
        record_bd_now = None
    return record_bd_now
