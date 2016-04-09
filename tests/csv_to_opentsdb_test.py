import unittest
from csv_to_opentsdb import *

class AddTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_add_1_1_should_be_2(self):
        self.assertEqual( add(1,1), 2)

# Unit
class PadZeroDateTest(unittest.TestCase):
    def test_date_3_should_03(self):
        self.assertEqual( pad_zero_date("3/10/2015"), "03/10/2015")
    def test_date_03_should_03(self):
        self.assertEqual( pad_zero_date("03/10/2015"), "03/10/2015")

class PadZeroTimeTest(unittest.TestCase):
    def test_time_0_should_00(self):
        self.assertEqual( pad_zero_time("0:45"), "00:45")
    def test_time_00_should_00(self):
        self.assertEqual( pad_zero_time("00:45"), "00:45")

#functional test
class PadZeroDatetimeTest(unittest.TestCase):
    def test_pad_zero_date_time(self):
        self.assertEqual( pad_zero_datetime("3/10/2015 0:45"), "03/10/2015 00:45")
    def test_pad_zero_date(self):
        self.assertEqual( pad_zero_datetime("3/10/2015 00:45"), "03/10/2015 00:45")
    def test_pad_zero_time(self):
        self.assertEqual( pad_zero_datetime("03/10/2015 0:45"), "03/10/2015 00:45")
    def test_not_pad_zero(self):
        self.assertEqual( pad_zero_datetime("03/10/2015 00:45"), "03/10/2015 00:45")

class RowConvertTest(unittest.TestCase):

    def test_row_convert1(self):
        self.assertEqual( row_convert(["13/10/2015 0:45", 5786]) , \
                                      [1444697100, 5786])
