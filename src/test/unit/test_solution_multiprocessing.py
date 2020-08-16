import json
import queue
import unittest
from multiprocessing import Queue
import time

from src.app.dto.SensorInstance import SensorInstance
from src.app.solutions.SolutionMultiProcessing import SolutionMultiProcessing

"""
These tests assume no other processes are writing to the database.
"""
class TestSolutionMultiprocessing(unittest.TestCase):

    """ Test items written the database can be accessed from the DB """
    def test_write(self):

        sensor_data_queue = Queue()
        max_queue_size = 3
        sensor_write_interval = 0
        n_processes = 1

        multiprocessing_solution = SolutionMultiProcessing()
        write_queue_processes = multiprocessing_solution.start_write_queue_process(sensor_data_queue,
                                                                                   sensor_write_interval, n_processes,
                                                                                 max_queue_size)

        for process in write_queue_processes:
            process.join()

        """ remove all items from the queue and test """
        self.assertEqual(json.loads(sensor_data_queue.get())['type'], SensorInstance.SENSOR_TYPE)
        self.assertEqual(json.loads(sensor_data_queue.get())['type'], SensorInstance.SENSOR_TYPE)
        self.assertEqual(json.loads(sensor_data_queue.get())['type'], SensorInstance.SENSOR_TYPE)

        """ An empty exception is thrown when queue is empty """
        with self.assertRaises(queue.Empty) as value_error:
            sensor_data_queue.get(timeout=1)
        self.assertEqual("", str(value_error.exception))

    """
    Test all values created by read process are processed by write process.
    This is a unit test, not inserting into Database.
    
    A "raise Empty" exception may thrown during execution of this test. If this occurs the test is not
    broken. Cannot gaurantee if queue is empty using empty() queue method. From the docs: "Because of 
    multithreading/multiprocessing semantics, this is not reliable.: src:https://docs.python.org/3/library/multiprocessing.html
    """
    def test_read(self):

        sensor_data_queue = Queue(5)
        max_queue_size = 3
        sensor_write_interval = 0
        sensor_read_interval = 0

        """starting more read that write operations in attempt to ensure (not gauranteed) queue is empty at end of 
        test """
        n_processes_write = 2
        n_processes_read = 5

        multiprocessing_solution = SolutionMultiProcessing()
        write_processes = multiprocessing_solution.start_write_queue_process(sensor_data_queue, sensor_write_interval,
                                                                             n_processes_write, max_queue_size)
        read_processes = multiprocessing_solution.start_read_queue_process(sensor_data_queue, sensor_read_interval,
                                                                           n_processes_read,
                                                                           False)
        print('Joining write_processes')
        for process in write_processes:
            process.join()

        print('Joining read_processes')
        for process in read_processes:
            process.join()

        self.assertTrue(len(write_processes), n_processes_write)
        self.assertTrue(len(read_processes), n_processes_read)

        # time.sleep(2)
        self.assertTrue(sensor_data_queue.empty())
