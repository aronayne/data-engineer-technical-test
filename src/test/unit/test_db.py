import mongoengine as me
import unittest

""" Inherit from me.Document which inherits save() operation """
class SensorInstanceContent(me.Document):
    pass

"""
Ideally use a multi db setup for test versus prod testing.
"""
class DBUnitTests(unittest.TestCase):

    def test_save(self):

        print('**** DBUnitTests - running test test_save ****')

        db_conn = me.connect(db='mongotest', host='mongomock://localhost')

        sensor_instance_content = SensorInstanceContent()
        sensor_instance_content.save()
        assert len(SensorInstanceContent.objects()) == 1

