import json
import unittest

from src.app.db.MongoDBConnection import MongoDBConnection
from src.app.dto.SensorInstanceBuilder import SensorInstanceBuilder
from src.app.encoder.SensorInstanceEncoder import SensorIntanceEncoder
from src.app.generator.SensorInstanceGenerator import SensorInstanceGenerator

"""
DB integrationtests test. If this test is located in 'integrationtests' folder it is ignored,
therefore is added to 'unit' folder.
"""
class DBIntegrationTests(unittest.TestCase):

    # Test a record inserted into the database is added.
    def test_insert(self):

        sensor_instance_generator = SensorInstanceGenerator()
        sensor_instance = next(sensor_instance_generator)
        temperature_c = 23
        sensor_instance_enriched = SensorInstanceBuilder(sensor_instance , temperature_c).build()
        sensor_instance_enriched_json = json.dumps(sensor_instance_enriched, cls=SensorIntanceEncoder)
        sensor_instance_enriched_object = json.loads(sensor_instance_enriched_json)

        with MongoDBConnection() as conn:
            conn.db.technicalTestCollection.insert_one(sensor_instance_enriched_object)
        find_query = { "id": sensor_instance_generator.get_guid()}
        with MongoDBConnection() as conn:
            results = conn.db.technicalTestCollection.find(find_query)
            assert len(list(results)) == 1

        with MongoDBConnection() as conn:
            conn.db.technicalTestCollection.delete_one(find_query)
            find_query = { "id": sensor_instance_generator.get_guid()}
            results = conn.db.technicalTestCollection.find(find_query)
            assert len(list(results)) == 0
