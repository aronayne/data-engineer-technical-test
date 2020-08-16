import unittest

from src.app.generator.TemperatureValueGenerator import TemperatureValueGenerator

"""
Test generated values from TemperatureValueGenerator
The TemperatureValueGenerator is_random_seed attribute is set to True which allows
for deterministic generator values.
"""
class TemperatureValueGeneratorTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temperatureValueGenerator = TemperatureValueGenerator(True)

    """ Test the generate temperature values """
    def test_generate_values(self):

        print('**** TemperatureValueGeneratorTests - running test test_test_generate_valueswrite ****')

        assert next(self.temperatureValueGenerator) == 89
        assert next(self.temperatureValueGenerator) == 96
        assert next(self.temperatureValueGenerator) == 86

