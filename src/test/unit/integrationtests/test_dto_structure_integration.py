import unittest
import json

from src.app.db.MongoDBConnection import MongoDBConnection
from src.app.dto.SensorInstance import SensorInstance
from src.app.dto.SensorInstanceBuilder import SensorInstanceBuilder
from src.app.encoder.SensorInstanceEncoder import SensorIntanceEncoder
from src.app.generator.SensorInstanceGenerator import SensorInstanceGenerator

"""
DB integrationtests test. If this test is located in 'integrationtests' folder it is ignored,
therefore is added to 'unit' folder.
"""
class DtoStructureIntegrationTests(unittest.TestCase):

    def test_dto_structure(self):

        print('**** DtoStructureIntegrationTests - running test test_dto_structure ****')

        sensor_instance_generator = SensorInstanceGenerator()
        sensor_instance = next(sensor_instance_generator)

        sensor_instance_enriched = SensorInstanceBuilder(sensor_instance , 23).build()

        sensor_instance_enriched_json = json.dumps(sensor_instance_enriched, cls=SensorIntanceEncoder)
        sensor_instance_enriched_object = json.loads(sensor_instance_enriched_json)
        with MongoDBConnection() as conn:
            conn.db.technicalTestCollection.insert_one(sensor_instance_enriched_object)
        find_query = { "id": sensor_instance_generator.get_guid()}
        with MongoDBConnection() as conn:
            results = conn.db.technicalTestCollection.find(find_query)
            top_level_results_keys = list(results[0].keys())
            content_level_results_keys = results[0]['content'].keys()

            self.assertTrue('id' in top_level_results_keys)
            self.assertTrue('type' in top_level_results_keys)
            self.assertTrue('content' in top_level_results_keys)

            self.assertTrue('temperature_f' in content_level_results_keys)
            self.assertTrue('time_of_measurement' in content_level_results_keys)
            self.assertTrue('temperature_c' in content_level_results_keys)

            self.assertEqual(results[0]['type'], SensorInstance.SENSOR_TYPE)

        with MongoDBConnection() as conn:
            conn.db.technicalTestCollection.delete_one(find_query)
            find_query = { "id": sensor_instance_generator.get_guid()}
            results = conn.db.technicalTestCollection.find(find_query)
            assert len(list(results)) == 0