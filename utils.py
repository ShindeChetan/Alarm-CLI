import datetime
import re

def parse_relative_time(time_str: str) -> datetime.timedelta:
    """
    Parses a relative time string and returns a timedelta.
    Supported formats: '10s', '5m', '2h', etc.
    """
    match = re.match(r"^(\d+)([smh])$", time_str.strip().lower())
    if not match:
        raise ValueError(f"Invalid relative time format: {time_str}. Use e.g. '10s', '5m', '1h'.")
    
    amount = int(match.group(1))
    unit = match.group(2)
    
    if unit == 's':
        return datetime.timedelta(seconds=amount)
    elif unit == 'm':
        return datetime.timedelta(minutes=amount)
    elif unit == 'h':
        return datetime.timedelta(hours=amount)

def parse_absolute_time(time_str: str, now: datetime.datetime = None) -> datetime.datetime:
    """
    Parses an absolute time string (HH:MM) and returns a datetime object for the next occurrence.
    """
    if now is None:
        now = datetime.datetime.now()
        
    match = re.match(r"^(\d{1,2}):(\d{2})$", time_str.strip())
    if not match:
        raise ValueError(f"Invalid absolute time format: {time_str}. Use HH:MM (24-hour format).")
        
    hour = int(match.group(1))
    minute = int(match.group(2))
    
    if not (0 <= hour <= 23) or not (0 <= minute <= 59):
        raise ValueError("Invalid time: hours must be 0-23 and minutes 0-59.")
        
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    # If the time has already passed today, set it for tomorrow
    if target <= now:
        target += datetime.timedelta(days=1)
        
    return target
