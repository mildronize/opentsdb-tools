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


    def case_3_real_situation_test(self):
        self.assertEqual(thread_scopes(946659600, 100000000,16), \
            [
            {'num':	6250000	, 'start': 	946659600	},
            {'num':	6250000	, 'start': 	977909600	},
            {'num':	6250000	, 'start': 	1009159600	},
            {'num':	6250000	, 'start': 	1040409600	},
            {'num':	6250000	, 'start': 	1071659600	},
            {'num':	6250000	, 'start': 	1102909600	},
            {'num':	6250000	, 'start': 	1134159600	},
            {'num':	6250000	, 'start': 	1165409600	},
            {'num':	6250000	, 'start': 	1196659600	},
            {'num':	6250000	, 'start': 	1227909600	},
            {'num':	6250000	, 'start': 	1259159600	},
            {'num':	6250000	, 'start': 	1290409600	},
            {'num':	6250000	, 'start': 	1321659600	},
            {'num':	6250000	, 'start': 	1352909600	},
            {'num':	6250000	, 'start': 	1384159600	},
            {'num':	6250000	, 'start': 	1415409600	}
            ])

class FindNumDataPointsPerRequestTest(unittest.TestCase):
    def find_dppr_1_test(self):
        self.assertEqual(find_num_dppr(0, 100, 80), 80 )
        self.assertEqual(find_num_dppr(1, 100, 80), 20 )

    def find_dppr_2_test(self):
        self.assertEqual(find_num_dppr(0, 240, 80), 80 )
        self.assertEqual(find_num_dppr(1, 240, 80), 80 )
        self.assertEqual(find_num_dppr(2, 240, 80), 80 )

    def find_dppr_3_test(self):
        self.assertEqual(find_num_dppr(0, 250, 80), 80 )
        self.assertEqual(find_num_dppr(1, 250, 80), 80 )
        self.assertEqual(find_num_dppr(2, 250, 80), 80 )
        self.assertEqual(find_num_dppr(3, 250, 80), 10 )

    def find_dppr_4_test(self):
        self.assertEqual(find_num_dppr(0, 100, 100), 100 )

# Unit
# class PadZeroDateTest(unittest.TestCase):
#     def test_date_3_should_03(self):
#         self.assertEqual( pad_zero_date("3/10/2015"), "03/10/2015")
#     #  def test_date_03_should_03(self):
#         #  self.assertEqual( pad_zero_date("03/10/2015"), "03/10/2015")
#     def test_date_13_should_13(self):
#         self.assertEqual( pad_zero_date("13/10/2015"), "13/10/2015")
