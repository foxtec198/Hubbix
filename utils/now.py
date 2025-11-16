from datetime import datetime as dt, timedelta, timezone

def now(hour:int = -3) -> dt:
    if hour: tz_brl = timezone(timedelta(hours=hour))
    else: tz_brl = timezone(timedelta(hours=-3))
    return dt.now().astimezone(tz_brl)