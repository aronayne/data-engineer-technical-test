from json import JSONEncoder

"""
Sub classes JSONEncoder to provide a custom implementation of the sensor instance
serialisation.
"""
class SensorIntanceEncoder(JSONEncoder):
    def default(self, object_to_serialize):
        serialized_object = object_to_serialize.__dict__
        return serialized_object