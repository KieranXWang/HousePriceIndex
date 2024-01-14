import datetime
import unittest

from src.utils import *


class TestFuncParseAddress(unittest.TestCase):
    def test_func_case_0(self):
        address = "207 Cedar St, Kirkland Washington"
        street_address, city, state = parse_address(address)
        self.assertEqual(street_address, "207 Cedar St")
        self.assertEqual(city, "Kirkland")
        self.assertEqual(state, "Washington")


class TestFuncBinarySearchFindInterval(unittest.TestCase):
    def test_func_case_0(self):
        arr = [1, 3, 5, 7, 9]
        target = 4
        left_index, right_index = binary_search_find_interval(arr, target)
        self.assertEqual(left_index, 1)
        self.assertEqual(right_index, 2)

    def test_func_case_1(self):
        arr = [1, 3, 5, 7, 9]
        target = 3
        left_index, right_index = binary_search_find_interval(arr, target)
        self.assertEqual(left_index, 1)
        self.assertEqual(right_index, 1)

    def test_func_case_2(self):
        arr = [1, 3, 5, 7, 9]
        target = 0
        left_index, right_index = binary_search_find_interval(arr, target)
        self.assertEqual(left_index, -1)
        self.assertEqual(right_index, 0)

    def test_func_case_3(self):
        arr = [1, 3, 5, 7, 9]
        target = 10
        left_index, right_index = binary_search_find_interval(arr, target)
        self.assertEqual(left_index, 4)
        self.assertEqual(right_index, 5)


class TestFuncConvertTimestampToText(unittest.TestCase):
    def test_func_case_0(self):
        dt = datetime.datetime(year=2023, month=10, day=1)
        ts = dt.timestamp()
        txt = convert_timestamp_to_readable_format(ts, show_hours=False)
        self.assertEqual('2023-10-01', txt)
