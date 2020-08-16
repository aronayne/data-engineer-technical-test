import uuid

from scipy.constants import convert_temperature

"""
Contains various utility functions used throughout the app.
"""
class AppUtils(object):

    """
    Return a globally unique identifier.
    As are serializing uuid convert to a String as uuid.uuid4() is not serializable
    """
    @staticmethod
    def get_uuid_str():
        return str(uuid.uuid4())

    """
    Return the degrees in celsius
    """
    @staticmethod
    def fahrenheit_to_celsius(degrees_in_fahrenheit):
        return int(convert_temperature(degrees_in_fahrenheit, 'Fahrenheit', 'Celsius'))
