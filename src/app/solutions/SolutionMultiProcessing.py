import json
import logging.config
import time
from multiprocessing import Process, Queue, Lock
from logging.config import dictConfig

from src.app.config import AppConfig
from src.app.config.logging.logging_config import logging_config
from src.app.db.MongoDBConnection import MongoDBConnection
from src.app.dto.SensorInstanceBuilder import SensorInstanceBuilder
from src.app.encoder.SensorInstanceEncoder import SensorIntanceEncoder
from src.app.generator.SensorInstanceGenerator import SensorInstanceGenerator
from src.app.generator.TemperatureValueGenerator import TemperatureValueGenerator
from src.app.utils.AppUtils import AppUtils

"""
Creates, reads and write data to the queue. Creates the random temperature generate and
enriches with temperature conversion.
"""
class SolutionMultiProcessing():

    """ Initialise class """
    def __init__(self):
        self.temperature_value_generator = TemperatureValueGenerator()
        self.sensor_instance_generator = SensorInstanceGenerator()
        """ Setup the logger for this class """
        dictConfig(logging_config)
        self.logger = logging.getLogger()
        self.logger.info('Initialising new instance of SolutionMultiProcessing')

    """ Read an instance of sensor data from the generator """
    def get_sensor_data(self):
        return next(self.sensor_instance_generator)

    """ Return the logger for this class """
    def get_logger(self):
        return self.logger

    """ 
    Enrich the sensor instance data with the Celsius attribute, temperature_c 
    
    Parameters
    ----------
    sensor_instance: The sensor data instance reading
    """
    def enrich_sensor_instance_data(self, sensor_instance):
        temperature_f = sensor_instance.content.temperature_f
        temperature_c = AppUtils.fahrenheit_to_celsius(temperature_f)
        return SensorInstanceBuilder(sensor_instance, temperature_c).build()

    """
    return the enriched sensor instance object 
    
    Parameters
    ----------
    sensor_instance: The sensor data instance reading
    """
    def get_enriched_sensor_data(self, sensor_instance):
        sensor_instance_enriched = self.enrich_sensor_instance_data(sensor_instance)
        return json.dumps(sensor_instance_enriched, cls=SensorIntanceEncoder)

    """ 
    Write sensor data to the shared queue 
    
    Parameters
    ----------
    sensor_data_queue: queue of sensor data items 
    time_interval: the time between readings of the sensor data generator
        max_queue_size: the max number of items to write to the sensor data queue for this process
    """
    def write_queue(self, sensor_data_queue, time_interval, max_queue_size):

        for write_queue_epoch in range(0, max_queue_size):
            sensor_instance = self.get_sensor_data()
            print("SolutionMultiProcessing - Sensor generated temperature_f value :",
                  str(sensor_instance.content.temperature_f))
            print('SolutionMultiProcessing - Writing item to queue')
            enriched_sensor_data = self.get_enriched_sensor_data(sensor_instance)
            sensor_data_queue.put(enriched_sensor_data)
            time.sleep(time_interval)

    """ 
    Insert an item into the Database

    Parameters
    ----------
    item: The item to be inserted into the database
    """
    def insert_into_db(self, item):
        with MongoDBConnection() as conn:
            print('SolutionMultiProcessing - Inserting sensor data into DB collection')
            conn.db.technicalTestCollection.insert_one(item)

    """ 
    Reading from the queue is tightly coupled with DB insertion, for loose coupling create a new separate queue 
    to store DB operations, a new set of thread processes reads from this queue 
    
    Using empty() check instead explicitly using an incrementing counter to check the queue size may result in a
    "raise Empty" exception. Using empty() does not guarantee if the queue is empty, from the docs: "Because of 
    multithreading/multiprocessing semantics, this is not reliable. 
    src:https://docs.python.org/3/library/multiprocessing.html
    
    Parameters
    ----------
    sensor_data_queue: queue of sensor data readings
    time_interval: the interval in seconds between reading items from the queue
    max_queue_size: the max number of items to read from the sensor data queue for this process
    insert_into_db: Boolean parameter, if True then insert items from the queue into database
    """
    def read_queue(self, sensor_data_queue, time_interval, max_queue_size, insert_into_db=True):
        read_item_count = 0
        while read_item_count < max_queue_size:
            read_item_count += 1
            print('SolutionMultiProcessing - Reading item from queue')
            item = sensor_data_queue.get(timeout=0.3)
            item_json = json.loads(item)
            if insert_into_db:
                print('Inserting sensor data into DB')
                self.insert_into_db(item_json)

        time.sleep(time_interval)

    """ 
    Starts the Process to write data to the sensor data queue 
    
    Parameters
    ----------
    sensor_data_queue: queue to write
    sensor_write_interval: time interval in seconds between write operations to the sensor_data_queue
    n_processes: number of concurrent processes to write to sensor_data_queue
    max_queue_size: the max number of items to write to sensor_data_queue for this process
    """
    def start_write_queue_process(self, sensor_data_queue, sensor_write_interval, n_processes, max_queue_size):

        self.logger.info('Number of write queue processes %s' , str(n_processes))
        self.logger.info('Max queue size: %s', str(n_processes * max_queue_size))
        self.logger.info("Start writing to queue process")

        write_processes = []
        for epoch in range(0 , n_processes):
            write_processes.append(Process(target=self.write_queue,
                                         args=(sensor_data_queue, sensor_write_interval,
                                               max_queue_size)))

        for write_process in write_processes:
            write_process.start()

        return write_processes

    """ 
    Starts the Process to read the data from the sensor data queue and write to database  
    
    Parameters
    ----------
    sensor_data_queue: queue to read
    sensor_read_interval: time interval in seconds between reads to the sensor_data_queue
    n_processes: number of concurrent processes to read from sensor_data_queue
    insert_into_db: Boolean to determine if items read from sensor_data_queue are inserted into database,
                    default is false.
    """
    def start_read_queue_process(self, sensor_data_queue, sensor_read_interval,
                                 n_processes, max_queue_size, insert_into_db=True):

        self.logger.info('Number of read queue processes %s', str(n_processes))
        self.logger.info('Start reading from Queue')

        read_processes = []
        for epoch in range(0 , n_processes):
            read_processes.append(Process(target=self.read_queue,
                                         args=(sensor_data_queue, sensor_read_interval,
                                               max_queue_size, insert_into_db)))

        for read_process in read_processes:
            read_process.start()

        return read_processes

if __name__ == '__main__':
    multiprocessing_solution = SolutionMultiProcessing()

    """
    A manager to hold the sensor_data_queue instead of sharing the sensor_data_queue between processes 
    but managers are 'slower than using shared memory' , 
    src : https://docs.python.org/2/library/multiprocessing.html#pipes-and-queues 
    """
    sensor_data_queue = Queue()

    """ Create and start the write queue processes """
    write_processes = multiprocessing_solution.start_write_queue_process(sensor_data_queue,
                                                                         AppConfig.sensor_write_interval_seconds,
                                                                         AppConfig.number_write_processes,
                                                                         AppConfig.max_size_per_process)

    """ Create and start the read queue processes """
    read_processes = multiprocessing_solution.start_read_queue_process(sensor_data_queue,
                                                                       AppConfig.sensor_read_interval_seconds,
                                                                       AppConfig.number_read_processes,
                                                                       AppConfig.max_size_per_process)

    """
    join all processes - write processes are joined prior to read processes
    """
    for process in write_processes + read_processes:
        multiprocessing_solution.logger.info('Joining process %s', process)
        process.join()
