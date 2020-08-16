"""
Modification of the sensor instance 'content' attribute to include celsius measurement.
"""


class SensorContentCelsius():
    def __init__(self, temperature_f, temperature_c, time_of_measurement):
        self.temperature_f = temperature_f
        self.temperature_c = temperature_c
        self.time_of_measurement = time_of_measurement
