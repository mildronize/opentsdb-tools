import unittest
from csv_to_opentsdb import *

class AddTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_add_1_1_should_be_2(self):
        self.assertEqual( add(1,1), 2)

# functional test
class RowConvertTest(unittest.TestCase):
    def test_row_convert1(self):
        self.assertEqual( row_convert( \
            ["13/10/2015 0:45", 5786]) , \
            [1444697100, 5786])
