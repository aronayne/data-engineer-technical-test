import time
from multiprocessing import Lock, Process, Queue, Pool
import unittest


class QueueFun():

    def write_data_to_queue(self, work_tasks, data):
        work_tasks.put(data)
        # print('work_tasks.empty()' , work_tasks.empty())

    def get_data_from_queue(self, work_tasks):
        return work_tasks.get()

    def writing_queue(self, work_tasks, name):
        while True:
            print("Writing to queue")

            work_tasks.put('1')
            time.sleep(1)

    def read_queue(self, work_tasks, name):
        while True:
            print("Reading from queue", work_tasks.empty())
            if work_tasks.empty():
                raise ValueError('Queue should not be empty')
            item = work_tasks.get()
            time.sleep(2)


class QueueFunTests(unittest.TestCase):

    def test_add_queue(self):
        q = QueueFun()
        work_tasks = Queue()
        q.write_data_to_queue(work_tasks , '1')
        time.sleep(1)
        self.assertFalse(work_tasks.empty())
        # print('work_tasks' , work_tasks.empty())

    def test_get_data_from_queue(self):
        q = QueueFun()
        work_tasks = Queue()
        q.write_data_to_queue(work_tasks, '1')
        queue_item = work_tasks.get()
        print('q is' , queue_item)
        self.assertEqual('1', queue_item)
        self.assertTrue(work_tasks.empty())

# q = Queue.Queue()
# print(q.empty())