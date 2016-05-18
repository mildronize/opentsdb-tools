import unittest
from flush_data import *

class FlushDataTest(unittest.TestCase):
    def flush_data_should_be_0(self):
        self.assertEqual( flush_data(5), 0)
        

# Unit
# class PadZeroDateTest(unittest.TestCase):
#     def test_date_3_should_03(self):
#         self.assertEqual( pad_zero_date("3/10/2015"), "03/10/2015")
#     #  def test_date_03_should_03(self):
#         #  self.assertEqual( pad_zero_date("03/10/2015"), "03/10/2015")
#     def test_date_13_should_13(self):
#         self.assertEqual( pad_zero_date("13/10/2015"), "13/10/2015")
