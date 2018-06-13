import pytz
from tzlocal import get_localzone
from datetime import datetime

def utc_to_local(utc_dt):
    local_tz = get_localzone()
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)

def isotime_utc_to_local(isotime_utc):
    return utc_to_local(parse_isotime(isotime_utc))

def parse_isotime(isotime):
   return datetime.strptime(isotime, '%Y-%m-%dT%H:%M:%S.%fZ')