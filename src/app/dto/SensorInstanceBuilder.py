from src.app.dto.SensorInstance import SensorInstance
from src.app.dto.SensorContentCelcius import SensorContentCelcius

"""
Models the addition of temperature_c attribute
"""
class SensorInstanceBuilder():
    def __init__(self, sensor_instance, temperature_c):
        self.sensor_instance = sensor_instance
        self.temperature_c = temperature_c

    """ Build and return the sensor instance """
    def build(self):

        temperature_c = self.temperature_c
        temperature_f = self.sensor_instance.content.temperature_f
        time_of_measurement = self.sensor_instance.content.time_of_measurement

        sensor_instance_content = SensorContentCelcius(temperature_f,
                                                       temperature_c,
                                                       time_of_measurement)

        sensor_instance_id = self.sensor_instance.id

        return SensorInstance(sensor_instance_id, sensor_instance_content)

