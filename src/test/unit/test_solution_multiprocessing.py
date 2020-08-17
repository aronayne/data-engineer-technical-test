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

        print('**** SolutionMultiProcessing - running test test_write ****')

        """ Setup """
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

        """ Assert """
        """ remove all items from the queue and test """
        self.assertEqual(json.loads(sensor_data_queue.get())['type'], SensorInstance.SENSOR_TYPE)
        self.assertEqual(json.loads(sensor_data_queue.get())['type'], SensorInstance.SENSOR_TYPE)
        self.assertEqual(json.loads(sensor_data_queue.get())['type'], SensorInstance.SENSOR_TYPE)
        """ An empty exception is thrown when queue is empty """
        with self.assertRaises(queue.Empty) as value_error:
            sensor_data_queue.get(timeout=1)
        self.assertEqual("", str(value_error.exception))

    """
    Test all items written to queue are read from queue.
    This is a unit test, not inserting into Database. 
    """
    def test_write_and_read(self):

        print('**** SolutionMultiProcessing - running test test_write_and_read ****')

        """ Setup """
        sensor_data_queue = Queue()
        max_queue_size_read = 2
        max_queue_size_write = 2
        sensor_write_interval = 0
        sensor_read_interval = 0
        n_processes_write = 2
        n_processes_read = 2
        multiprocessing_solution = SolutionMultiProcessing()
        write_processes = multiprocessing_solution.start_write_queue_process(sensor_data_queue, sensor_write_interval,
                                                                             n_processes_write, max_queue_size_write)
        read_processes = multiprocessing_solution.start_read_queue_process(sensor_data_queue, sensor_read_interval,
                                                                           n_processes_read,  max_queue_size_read,
                                                                           False)
        for process in write_processes + read_processes:
            print('**** SolutionMultiProcessing - Joining process %s', process , '****')
            process.join()

        """ Assert """
        self.assertTrue(len(write_processes), n_processes_write)
        self.assertTrue(len(read_processes), n_processes_read)
        self.assertTrue(sensor_data_queue.empty())

