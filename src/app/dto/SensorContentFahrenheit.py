"""
Model 'content' attribute to include Fahrenheit measurement.
"""

class SensorContentFahrenheit():
    def __init__(self, temperature_f, time_of_measurement):
        self.temperature_f = temperature_f
        self.time_of_measurement = time_of_measurement
