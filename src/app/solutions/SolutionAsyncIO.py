import asyncio
import functools
import json
import logging.config

import rx

from src.app.config import AppConfig
from src.app.config.logging.logging_config import logging_config
from src.app.db.MongoDBConnection import MongoDBConnection
from src.app.dto.SensorInstanceBuilder import SensorInstanceBuilder
from src.app.encoder.SensorInstanceEncoder import SensorIntanceEncoder
from src.app.generator.SensorInstanceGenerator import SensorInstanceGenerator
from src.app.generator.TemperatureValueGenerator import TemperatureValueGenerator
from src.app.utils.AppUtils import AppUtils
from logging.config import dictConfig

"""
Responsible for setting up the observer and subscriber 
"""
class SolutionAsyncIO():

    def __init__(self):
        self.temperature_value_generator = TemperatureValueGenerator()
        self.sensor_instance_generator = SensorInstanceGenerator()
        """ Setup the logger for this class """
        dictConfig(logging_config)
        self.logger = logging.getLogger()

    """ Invoke an instance of the temperature value generator """
    def random_generator(self):
        return next(self.temperature_value_generator)

    """ Create the observable """
    def create_observable(self, iter, loop):
        """
        setup the observable

        Parameters
        ----------
        observer: the observer for this subsriber
        scheduler: scheduler provides a thread for each subscription to do work
        """
        def on_subscribe(observer, scheduler):
            async def call_item():
                async for i in iter:
                    observer.on_next(i)
                loop.call_soon(observer.on_completed)
            asyncio.ensure_future(call_item(), loop=loop)
        return rx.create(on_subscribe)

    def get_sensor_instance_data(self):
        return next(self.sensor_instance_generator)

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
    Insert an item into the Database

    Parameters
    ----------
    item: The item to be inserted into the database
    """
    def insert_into_db(self, item):
        with MongoDBConnection() as conn:
            self.logger.info('Inserting sensor data into DB collection')
            conn.db.technicalTestCollection.insert_one(item)

    """ Return a sensor reading """
    async def get_sensor_data_iter(self, max_queue_size, sensor_write_interval_seconds):
        for write_queue_epoch in range(0, max_queue_size):

            sensor_instance = self.get_sensor_instance_data()
            self.logger.info("Sensor generated temperature_f value : %s" , str(sensor_instance.content.temperature_f))

            enriched_sensor_data = self.get_enriched_sensor_data(sensor_instance)
            yield enriched_sensor_data
            await asyncio.sleep(sensor_write_interval_seconds)

    """ 
    Read an item from the queue and insert to DB
    
    Reading from the queue is tightly coupled with DB insertion.
    It appears easier to achieve loose coupling using asyncio as can return a queue with
    the DB inserts.
    
    Parameters
    ----------
    sensor_data_queue: queue of sensor data readings
    time_interval: the interval in seconds between reading items from the queue
    insert_into_db: Boolean parameter, if True then insert items from the queue into database
    """
    async def read_queue(self, sensor_data_queue, time_interval, insert_into_db=True):
        while not sensor_data_queue.empty():
            self.logger.info('Reading sensor data from queue')
            item_to_write_to_db = await sensor_data_queue.get()
            item_json = json.loads(item_to_write_to_db)
            if insert_into_db:
                self.insert_into_db(item_json)
            await asyncio.sleep(time_interval)

    """ 
    Write an item to the asyncio queue

    Parameters
    ----------
    param sensor_data_queue: queue of sensor data readings
    loop: from asyncio docs "Coroutines will be wrapped in a future and scheduled in the event
    loop"
    max_queue_size: the max items to write to the queue
    time_interval: the interval in seconds between writing items to the queue
    """
    async def write_queue(self, sensor_data_queue, loop, max_queue_size, time_interval):
        done = asyncio.Future()

        def on_completed():
            done.set_result(0)

        def write_item_to_queue(sensor_data):
            self.logger.info('Writing sensor data reading to queue ')
            sensor_data_queue.put_nowait(sensor_data)

        observable = self.create_observable(self.get_sensor_data_iter(max_queue_size, time_interval),
                                            loop)
        subscriber = observable.subscribe(
            on_next=write_item_to_queue,
            on_error=lambda error: self.logger.error("error: {}".format(error)),
            on_completed=on_completed,
        )
        await done
        subscriber.dispose()

    # async def read_queue(self, sensor_data_queue, sensor_read_interval_seconds):
    #     await self.read_item_from_queue(sensor_data_queue, sensor_read_interval_seconds)


if __name__ == '__main__':
    """ initialise the sensor data queue """
    sensor_data_queue = asyncio.Queue()

    solution_async_io = SolutionAsyncIO()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(solution_async_io.write_queue(sensor_data_queue, loop, AppConfig.max_queue_size,
                                                          AppConfig.sensor_write_interval_seconds))

    loop.run_until_complete(solution_async_io.read_queue(sensor_data_queue, AppConfig.sensor_read_interval_seconds))

