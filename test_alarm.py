import unittest
import datetime
from utils import parse_relative_time, parse_absolute_time
from alarm import Alarm

class TestTimeParsing(unittest.TestCase):
    
    def test_parse_relative_time_seconds(self):
        delta = parse_relative_time("10s")
        self.assertEqual(delta.total_seconds(), 10)
        
    def test_parse_relative_time_minutes(self):
        delta = parse_relative_time("5m")
        self.assertEqual(delta.total_seconds(), 300)
        
    def test_parse_relative_time_hours(self):
        delta = parse_relative_time("2h")
        self.assertEqual(delta.total_seconds(), 7200)
        
    def test_parse_relative_time_invalid(self):
        with self.assertRaises(ValueError):
            parse_relative_time("10d")
            
    def test_parse_absolute_time_today(self):
        now = datetime.datetime(2023, 1, 1, 10, 0, 0)
        target = parse_absolute_time("15:30", now)
        self.assertEqual(target.year, 2023)
        self.assertEqual(target.month, 1)
        self.assertEqual(target.day, 1)
        self.assertEqual(target.hour, 15)
        self.assertEqual(target.minute, 30)

    def test_parse_absolute_time_tomorrow(self):
        now = datetime.datetime(2023, 1, 1, 16, 0, 0)
        target = parse_absolute_time("15:30", now)
        self.assertEqual(target.year, 2023)
        self.assertEqual(target.month, 1)
        self.assertEqual(target.day, 2)
        self.assertEqual(target.hour, 15)
        self.assertEqual(target.minute, 30)
        
    def test_parse_absolute_time_invalid(self):
        now = datetime.datetime(2023, 1, 1, 10, 0, 0)
        with self.assertRaises(ValueError):
            parse_absolute_time("25:30", now)
        with self.assertRaises(ValueError):
            parse_absolute_time("15:60", now)

class TestAlarm(unittest.TestCase):
    
    def test_time_remaining(self):
        now = datetime.datetime.now()
        target = now + datetime.timedelta(seconds=10)
        alarm = Alarm(target)
        
        remaining = alarm.time_remaining()
        # Due to execution time, it might be slightly less than 10, but should be > 9
        self.assertTrue(9 < remaining.total_seconds() <= 10)

if __name__ == '__main__':
    unittest.main()
