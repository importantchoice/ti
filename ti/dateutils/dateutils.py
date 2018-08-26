import pytz
import os
import re

from tzlocal import get_localzone
from datetime import datetime, timedelta


from ti.exceptions import *

TI_TODAY_ENV_VAR = "TI_CURRENT_DAY"

def get_local_timezone():
    return get_localzone()


def utc_to_local(utc_dt):
    local_tz = get_local_timezone()
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)


def isotime_utc_to_local(isotime_utc):
    return utc_to_local(parse_isotime(isotime_utc))


def parse_isotime(isotime_str):
    return datetime.strptime(isotime_str, '%Y-%m-%dT%H:%M:%S.%fZ')


def to_datetime(timestr):
    return parse_engtime(timestr).isoformat() + 'Z'


def local_to_utc(local_dt):
    local_dt_dst = get_local_timezone().localize(local_dt)
    utc_dt = local_dt_dst.astimezone(pytz.utc)
    return utc_dt.replace(tzinfo=None)


def get_current_day():
    today_value = os.getenv(TI_TODAY_ENV_VAR, None)
    return today_value


def parse_engtime(timestr):
    now = datetime.utcnow()
    if not timestr or timestr.strip() == 'now':
        return now

    try:
        settime = datetime.strptime(timestr, "%H:%M")
        x = now.replace(hour=settime.hour, minute=settime.minute, second=0, microsecond=1)
        if get_current_day() is not None:
            currentday = datetime.strptime(get_current_day(), "%d.%m.%Y")
            y = x.replace(day=currentday.day, month=currentday.month, year=currentday.year)
            return local_to_utc(y)
        return local_to_utc(x)
    except Exception as e:
        print(e)
        # pass

    match = re.match(r'(\d+|a) \s* (s|secs?|seconds?) \s+ ago $',
                     timestr, re.X)
    if match is not None:
        n = match.group(1)
        seconds = 1 if n == 'a' else int(n)
        diff = now - timedelta(seconds=seconds)
        print(diff)
        print(isotime_utc_to_local(diff.isoformat() + 'Z'))
        return now - timedelta(seconds=seconds)

    match = re.match(r'(\d+|a) \s* (mins?|minutes?) \s+ ago $', timestr, re.X)
    if match is not None:
        n = match.group(1)
        minutes = 1 if n == 'a' else int(n)
        return now - timedelta(minutes=minutes)

    match = re.match(r'(\d+|a|an) \s* (hrs?|hours?) \s+ ago $', timestr, re.X)
    if match is not None:
        n = match.group(1)
        hours = 1 if n in ['a', 'an'] else int(n)
        return now - timedelta(hours=hours)

    raise BadTime("Don't understand the time %r" % (timestr,))


def timegap(start_time, end_time):
    diff = end_time - start_time

    mins = diff.total_seconds() // 60

    if mins == 0:
        return 'less than a minute'
    elif mins == 1:
        return 'a minute'
    elif mins < 44:
        return '{} minutes'.format(mins)
    elif mins < 89:
        return 'about an hour'
    elif mins < 1439:
        return 'about {} hours'.format(mins // 60)
    elif mins < 2519:
        return 'about a day'
    elif mins < 43199:
        return 'about {} days'.format(mins // 1440)
    elif mins < 86399:
        return 'about a month'
    elif mins < 525599:
        return 'about {} months'.format(mins // 43200)
    else:
        return 'more than a year'