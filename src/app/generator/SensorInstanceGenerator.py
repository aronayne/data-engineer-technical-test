from collections.abc import Generator
from datetime import datetime
from src.app.dto.SensorInstance import SensorInstance
from src.app.dto.SensorContentFahrenheit import SensorContentFahrenheit
from src.app.generator.TemperatureValueGenerator import TemperatureValueGenerator
from src.app.utils.AppUtils import AppUtils

"""
Generator of sensor data which invokes the random value temperature value generator
"""
class SensorInstanceGenerator(Generator):
    def __init__(self):
        self.f = TemperatureValueGenerator()
        self.guid = None

    def send(self, ignored_arg):

        random_f_temp = next(self.f)
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%dT%H:%M:%S")

        sensor_instance_fahrenheit = SensorContentFahrenheit(random_f_temp, dt_string)

        self.guid = AppUtils.get_uuid_str()
        sensor_instance = SensorInstance(self.guid, sensor_instance_fahrenheit)

        return sensor_instance

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

    """ Return the guid for the instance"""
    def get_guid(self):
        return self.guid
