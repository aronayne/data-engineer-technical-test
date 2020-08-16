import asyncio
import unittest

from src.app.solutions.SolutionAsyncIO import SolutionAsyncIO

"""
These tests assume no other processes are writing to the database.
"""
class TestSolutionAsyncIo(unittest.TestCase):

    """ Test items written the database can be accessed from the DB """
    def test_solution_asyncio_write(self):

        print('**** TestSolutionAsyncIo - running test test_solution_asyncio_write ****')

        time_interval = 0
        max_queue_size = 3

        """ initialise the sensor data queue """
        sensor_data_queue = asyncio.Queue()

        solution_async_io = SolutionAsyncIO()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(solution_async_io.write_queue(sensor_data_queue, loop, max_queue_size,
                                                              time_interval))
        self.assertTrue(sensor_data_queue.qsize() == 3)

        loop.run_until_complete(solution_async_io.read_queue(sensor_data_queue, time_interval))
        self.assertTrue(sensor_data_queue.qsize() == 0)
