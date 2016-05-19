import unittest
from flush_data import *


class FlushDataTest(unittest.TestCase):
    def flush_data_should_be_0(self):
        self.assertEqual( flush_data(5), 0)

class ThreadScopesTest(unittest.TestCase):

    def case_1_exact_division_with_1_thread_test(self):
        self.assertEqual(thread_scopes(0, 10,1), \
            [
            {'num': 10, 'start': 0}
            ]
        )

    def case_1_exact_division_with_2_threads_test(self):
        self.assertEqual(thread_scopes(0, 10,2), \
            [
            {'num': 5, 'start': 0},
            {'num': 5, 'start': 25}
            ]
        )
    def case_1_exact_division_with_3_threads_test(self):
        self.assertEqual(thread_scopes(0, 15,3), \
            [
            {'num': 5, 'start': 0},
            {'num': 5, 'start': 25},
            {'num': 5, 'start': 50}
            ]
        )
    def case_2_non_exact_division_test(self):
        self.assertEqual(thread_scopes(0, 10,3), \
            [
            {'num': 3, 'start': 0},
            {'num': 3, 'start': 15},
            {'num': 4, 'start': 30}
            ]
        )

    def case_1_exact_division_with_1_thread_and_start_wo_zero_test(self):
        self.assertEqual(thread_scopes(1, 10,1), \
            [
            {'num': 10, 'start': 1}
            ]
        )

    def case_1_exact_division_with_2_threads_and_start_wo_zero_test(self):
        self.assertEqual(thread_scopes(1, 10,2), \
            [
            {'num': 5, 'start': 1},
            {'num': 5, 'start': 26}
            ]
        )
    def case_1_exact_division_with_3_threads_and_start_wo_zero_test(self):
        self.assertEqual(thread_scopes(1, 15,3), \
            [
            {'num': 5, 'start': 1},
            {'num': 5, 'start': 26},
            {'num': 5, 'start': 51}
            ]
        )
    def case_2_non_exact_division_and_start_wo_zero_test(self):
        self.assertEqual(thread_scopes(1, 10,3), \
            [
            {'num': 3, 'start': 1},
            {'num': 3, 'start': 16},
            {'num': 4, 'start': 31}
            ]
        )



# Unit
# class PadZeroDateTest(unittest.TestCase):
#     def test_date_3_should_03(self):
#         self.assertEqual( pad_zero_date("3/10/2015"), "03/10/2015")
#     #  def test_date_03_should_03(self):
#         #  self.assertEqual( pad_zero_date("03/10/2015"), "03/10/2015")
#     def test_date_13_should_13(self):
#         self.assertEqual( pad_zero_date("13/10/2015"), "13/10/2015")
