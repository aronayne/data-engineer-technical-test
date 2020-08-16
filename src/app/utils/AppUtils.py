import uuid

from scipy.constants import convert_temperature

from src.app.config import AppConfig

"""
Utility class
"""
class AppUtils(object):

    """
    Return a globally unique identifier.
    As are serializing uuid convert to a String as uuid is not serializable
    """
    @staticmethod
    def get_uuid_str():
        return str(uuid.uuid4())

    """
    Return the degrees in celcius
    """
    @staticmethod
    def fahrenheit_to_celsius(degrees_in_fahrenheit):
        return round(convert_temperature(degrees_in_fahrenheit, 'Fahrenheit', 'Celsius') , AppConfig.precision_value)
