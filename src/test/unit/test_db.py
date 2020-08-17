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

        """ Setup """
        db_conn = me.connect(db='mongotest', host='mongomock://localhost')
        sensor_instance_content = SensorInstanceContent()
        sensor_instance_content.save()

        """ Assert """
        assert len(SensorInstanceContent.objects()) == 1

