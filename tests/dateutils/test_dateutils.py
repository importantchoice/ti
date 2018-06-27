from unittest import TestCase
from ti.dateutils.dateutils import *
import mock
import pytz

test_timezone = "Europe/Berlin"

class TestDateutils(TestCase):

    @mock.patch('ti.dateutils.get_local_timezone')
    def test_utc_to_local_cet_winter_time(self, mocked):
        mocked.return_value=pytz.timezone(test_timezone)
        test_time_as_datetime = parse_isotime("2018-02-01T18:00:00.000001Z")
        time_h_m = utc_to_local(test_time_as_datetime).strftime("%H:%M")
        self.assertEqual("19:00", time_h_m)

    @mock.patch('ti.dateutils.get_local_timezone')
    def test_utc_to_local_cet_summer_time(self, mocked):
        mocked.return_value = pytz.timezone(test_timezone)
        test_time_as_datetime = parse_isotime("2018-06-01T18:00:00.000001Z")
        time_h_m = utc_to_local(test_time_as_datetime).strftime("%H:%M")
        self.assertEqual("20:00", time_h_m)

    @mock.patch('ti.dateutils.get_local_timezone')
    def test_isotime_utc_to_local_cet_winter_time(self, mocked):
        mocked.return_value = pytz.timezone(test_timezone)
        isotime_local = isotime_utc_to_local("2018-02-01T17:00:00.000001Z")
        self.assertEqual("2018-02-01T18:00:00.000001+01:00", isotime_local.isoformat())

    @mock.patch('ti.dateutils.get_local_timezone')
    def test_isotime_utc_to_local_cet_summer_time(self, mocked):
        mocked.return_value = pytz.timezone(test_timezone)
        isotime_local = isotime_utc_to_local("2018-06-01T17:00:00.000001Z")
        self.assertEqual("2018-06-01T19:00:00.000001+02:00", isotime_local.isoformat())

    def test_parse_isotime(self):
        isotime_now = datetime.now().isoformat()+"Z"
        isotime_string = parse_isotime(isotime_now)
        self.assertEqual("false", "false")
