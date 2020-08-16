import json
import logging.config
import time
from multiprocessing import Process, Queue
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

    """ Read an instance of sensor data from the generator """
    def get_sensor_data(self):
        return next(self.sensor_instance_generator)

    """ Return the logger for this class """
    def get_logger(self):
        return self.logger

    """ 
    Enrich the sensor instance data with temperature_c 
    
    Parameters
    ----------
    sensor_instance: The sensor instance
    """
    def enrich_sensor_instance_data(self, sensor_instance):
        temperature_f = sensor_instance.content.temperature_f
        temperature_c = AppUtils.fahrenheit_to_celsius(temperature_f)
        return SensorInstanceBuilder(sensor_instance, temperature_c).build()

    """
    return the enriched sensor instance object 
    
    Parameters
    ----------
    sensor_instance: the sensor data instance
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
    max_queue_size: the maximum size of the sensor data queue to populate
    """
    def write_queue(self, sensor_data_queue, time_interval, max_queue_size):

        for write_queue_epoch in range(0, max_queue_size):
            sensor_instance = self.get_sensor_data()
            self.logger.info("Sensor generated temperature_f value : %s" , str(sensor_instance.content.temperature_f))
            sensor_data_queue.put(self.get_enriched_sensor_data(sensor_instance))
            time.sleep(time_interval)

    """ 
    Insert an item into the Database

    Parameters
    ----------
    item: The item to be inserted into the database
    """
    def insert_into_db(self, item):
        with MongoDBConnection() as conn:
            self.logger.info('Inserting sensor data into DB collection')
            conn.db.technicalTestCollection.insert_one(item)

    """ 
    Check for empty as the read thread can start before the write thread 
    Reading from the queue is tightly coupled with DB insertion, for loose coupling create a new separate queue 
    to store DB operations, a new set of thread processes reads from this queue 
    
    Parameters
    ----------
    sensor_data_queue: queue of sensor data readings
    time_interval: the interval in seconds between reading items from the queue
    insert_into_db: Boolean parameter, if True then insert items from the queue into database
    """
    def read_queue(self, sensor_data_queue, time_interval, insert_into_db=True):
        while not sensor_data_queue.empty():
            self.logger.info('Getting item from queue')
            item = sensor_data_queue.get(timeout=0.3)
            item_json = json.loads(item)
            if insert_into_db:
                self.logger.info('Inserting sensor data into DB')
                self.insert_into_db(item_json)

            time.sleep(time_interval)

    """ 
    Starts the Process to write data to the sensor data queue 
    
    Parameters
    ----------
    sensor_data_queue: queue to write
    sensor_write_interval: time interval in seconds between write operations to the sensor_data_queue
    n_processes: number of concurrent processes to write to sensor_data_queue
    max_queue_size: the max number of items to write to sensor_data_queue
    """
    def start_write_queue_process(self, sensor_data_queue, sensor_write_interval, n_processes, max_queue_size):

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
                                 n_processes, insert_into_db=True):

        self.logger.info('Start reading from Queue')

        read_processes = []
        for epoch in range(0 , n_processes):
            read_processes.append(Process(target=self.read_queue,
                                         args=(sensor_data_queue, sensor_read_interval,
                                               insert_into_db)))

        for read_process in read_processes:
            read_process.start()

        return read_processes

if __name__ == '__main__':
    multiprocessing_solution = SolutionMultiProcessing()
    sensor_data_queue = Queue()

    """ Create and start the write queue processes """
    write_processes = multiprocessing_solution.start_write_queue_process(sensor_data_queue,
                                                                         AppConfig.sensor_write_interval_seconds,
                                                                         AppConfig.number_write_processes,
                                                                         AppConfig.max_queue_size)

    """ Create and start the read queue processes """
    read_processes = multiprocessing_solution.start_read_queue_process(sensor_data_queue,
                                                                       AppConfig.sensor_read_interval_seconds,
                                                                       AppConfig.number_read_processes)

    """ 
    join all processes - write processes are joined prior to read processes
    """
    for process in write_processes + read_processes:
        multiprocessing_solution.logger.info('In SolutionMultiProcessing - Joining process %s', process)
        process.join()
