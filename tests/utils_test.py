import unittest
from utils import *

class UtilsTest(unittest.TestCase):
    def datetime_string_to_timestamp_test(self):
        self.assertEqual( datetime_string_to_timestamp("01/01/2000 0:00"), 946659600)
