import threading
import random

random.seed(0)
TOTAL = []

class worker (threading.Thread):
    def __init__(self, threadID, name, number_data_points):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.number_data_points = number_data_points

    def run(self):
        for dp in range(self.number_data_points):
            TOTAL[self.threadID-1] += random.randint(1000, 2000)

def simulate_opentsdb_calc(number_data_points, num_threads):
    threads = []
    scopes = calculate_scope_of_each_thread(number_data_points, num_threads)
    for scope in range(len(scopes)):
        TOTAL.append(0)
    for i, scope in enumerate(scopes):
        threads.append(worker(i+1, "Thread " + str(i+1), scope))
        threads[i].start()

    for thread in threads:
        thread.join()
    print("Gathering all data")
    total = 0
    for i, scope in enumerate(scopes):
        total += TOTAL[i]
    print("Sum is ", total)
    return total

def calculate_scope_of_each_thread(number_data_points, num_threads):
    result = []
    for i in range(num_threads):
        # last looping
        if i+1 == num_threads and num_threads != 1:
            result.append(int(number_data_points/num_threads) + number_data_points%num_threads)
        else:
            result.append(int(number_data_points/num_threads))
    return result
