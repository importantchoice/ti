from unittest import TestCase
from dateutils import *

class TestDateutils(TestCase):
    def test_utc_to_local(self):


        start_time = utc_to_local(parse_isotime("2018-03-01T18:00:00.000001Z")).strftime("%H:%M")
        self.assertEqual(start_time, "19:00")
