import unittest

from opentsdb_importer.flush_data import *

class DataGeneratorTest(unittest.TestCase):
    def dataGenerator_5017_numthreads_16_test(self):
        assigned_dps = 5017
        num_threads = 16
        result_dps = DataGenerator(write_mode = None,
                                   start_timestamp = 946659600, \
                                   number_data_points = assigned_dps, \
                                   interval = 5, \
                                   num_threads = num_threads, \
                                   start_val = 5000, \
                                   end_val = 6000, \
                                   tags = [
                                      "location=hatyai"
                                   ]).run()
        self.assertEqual(assigned_dps, result_dps)
    def dataGenerator_5017_numthreads_8_test(self):
        assigned_dps = 5017
        num_threads = 16
        result_dps = DataGenerator(write_mode = None,
                                   start_timestamp = 946659600, \
                                   number_data_points = assigned_dps, \
                                   interval = 5, \
                                   num_threads = num_threads, \
                                   start_val = 5000, \
                                   end_val = 6000, \
                                   tags = [
                                      "location=hatyai"
                                   ]).run()
        self.assertEqual(assigned_dps, result_dps)
    def dataGenerator_5017_numthreads_2_test(self):
        assigned_dps = 5017
        num_threads = 16
        result_dps = DataGenerator(write_mode = None,
                                   start_timestamp = 946659600, \
                                   number_data_points = assigned_dps, \
                                   interval = 5, \
                                   num_threads = num_threads, \
                                   start_val = 5000, \
                                   end_val = 6000, \
                                   tags = [
                                      "location=hatyai"
                                   ]).run()
        self.assertEqual(assigned_dps, result_dps)

# class DataGeneratorWorker(unittest.TestCase):
#     import queue
#     def dataGeneratorWorker_597_test(self):
#         assigned_dps = 597
#         q = queue.Queue()
#         worker_configs = {
#             "start_timestamp": 0,
#             "number_data_points" : assigned_dps,
#             "interval": 5,
#             "start_val": 5000,
#             "end_val": 6000,
#             "tags": convert_tags_string_to_dict(["location=hatyai"])
#         }
#         threads = DataGeneratorWorker(threadID = 0, \
#                                       worker_configs = worker_configs, \
#                                       q = q)
#         threads.join()
#         result_dps = int(q.get())
#         self.assertEqual(assigned_dps, result_dps)

# unit tests

class ThreadScopesTest(unittest.TestCase):

    def case_1_exact_division_with_1_thread_test(self):
        self.assertEqual(calculate_scope_of_each_thread(0, 10,1,5), \
            [
            {'num': 10, 'start': 0}
            ]
        )

    def case_1_exact_division_with_2_threads_test(self):
        self.assertEqual(calculate_scope_of_each_thread(0, 10,2,5), \
            [
            {'num': 5, 'start': 0},
            {'num': 5, 'start': 25}
            ]
        )
    def case_1_exact_division_with_3_threads_test(self):
        self.assertEqual(calculate_scope_of_each_thread(0, 15,3,5), \
            [
            {'num': 5, 'start': 0},
            {'num': 5, 'start': 25},
            {'num': 5, 'start': 50}
            ]
        )
    def case_2_non_exact_division_test(self):
        self.assertEqual(calculate_scope_of_each_thread(0, 10,3,5), \
            [
            {'num': 3, 'start': 0},
            {'num': 3, 'start': 15},
            {'num': 4, 'start': 30}
            ]
        )

    def case_1_exact_division_with_1_thread_and_start_wo_zero_test(self):
        self.assertEqual(calculate_scope_of_each_thread(1, 10,1,5), \
            [
            {'num': 10, 'start': 1}
            ]
        )

    def case_1_exact_division_with_2_threads_and_start_wo_zero_test(self):
        self.assertEqual(calculate_scope_of_each_thread(1, 10,2,5), \
            [
            {'num': 5, 'start': 1},
            {'num': 5, 'start': 26}
            ]
        )
    def case_1_exact_division_with_3_threads_and_start_wo_zero_test(self):
        self.assertEqual(calculate_scope_of_each_thread(1, 15,3,5), \
            [
            {'num': 5, 'start': 1},
            {'num': 5, 'start': 26},
            {'num': 5, 'start': 51}
            ]
        )
    def case_2_non_exact_division_and_start_wo_zero_test(self):
        self.assertEqual(calculate_scope_of_each_thread(1, 10,3,5), \
            [
            {'num': 3, 'start': 1},
            {'num': 3, 'start': 16},
            {'num': 4, 'start': 31}
            ]
        )


    def case_3_real_situation_test(self):
        self.assertEqual(calculate_scope_of_each_thread(946659600, 100000000,16,5), \
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

class ConvertTagsStringToDictTest(unittest.TestCase):
    def case_length_1_test(self):
        self.assertEqual(convert_tags_string_to_dict([
            "location=hatyai"
        ]), {
            'location': 'hatyai'
        })

    # def case_length_2_test(self):
    #     self.assertEqual(convert_tags_string_to_dict([
    #         "location=hatyai" , "location=yala"
    #     ]), {
    #         'location': 'hatyai',
    #         'location': 'yala',
    #     })
