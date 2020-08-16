"""
Model the SensorInstance 'has a' relationship with 'content' attribute.
"""
class SensorInstance() :

    SENSOR_TYPE = "Sensor"

    def __init__(self, id, content):

        self.id = id
        self.content = content
        self.type = SensorInstance.SENSOR_TYPE
