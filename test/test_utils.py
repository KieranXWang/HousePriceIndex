import unittest

from src.utils import *


class TestFuncParseAddress(unittest.TestCase):
    def test_func_case_0(self):
        address = "207 Cedar St, Kirkland Washington"
        street_address, city, state = parse_address(address)
        self.assertEqual(street_address, "207 Cedar St")
        self.assertEqual(city, "Kirkland")
        self.assertEqual(state, "Washington")
