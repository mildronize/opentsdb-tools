import unittest

class Calculate_scope_of_each_threadTest(unittest.TestCase):

    def num_dp_100_nthread_1_test(self):
        from opentsdb_importer.simulate_opentsdb_calc import calculate_scope_of_each_thread
        self.assertEqual(calculate_scope_of_each_thread(100,1), [100])

    def num_dp_100_nthread_2_test(self):
        from opentsdb_importer.simulate_opentsdb_calc import calculate_scope_of_each_thread
        self.assertEqual(calculate_scope_of_each_thread(100,2), [50,50])

    def num_dp_100_nthread_3_test(self):
        from opentsdb_importer.simulate_opentsdb_calc import calculate_scope_of_each_thread
        self.assertEqual(calculate_scope_of_each_thread(100,3), [33,33,34])
