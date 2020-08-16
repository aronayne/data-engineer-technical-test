import random
from collections.abc import Generator

"""
Generates a random temperature reading value in the range of
80 - 120. To aid testing deterministic results can be returned via setting the
is_random_seed=True
"""
class TemperatureValueGenerator(Generator):
    def __init__(self, is_random_seed=False):
        self.number_values = 1
        if is_random_seed :
            random.seed(20)

    def send(self, ignored_arg):
        return random.sample(range(80 , 120), self.number_values)[0]

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

