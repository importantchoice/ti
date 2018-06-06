import pytz
from tzlocal import get_localzone
from datetime import datetime

class DateUtils():

    @staticmethod
    def utc_to_local(utc_dt):


        local_tz = get_localzone()
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
        return local_tz.normalize(local_dt)

    @staticmethod
    def isotime_utc_to_local(isotime_utc):
        return utc_to_local(self.parse_isotime(isotime_utc))

    @staticmethod
    def parse_isotime(isotime):
        return datetime.strptime(isotime, '%Y-%m-%dT%H:%M:%S.%fZ')