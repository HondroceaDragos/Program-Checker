from ..abs_generator._abs_generator import Generator

import random

class LargeTestGenerator(Generator):
    @classmethod
    def create_target_sum(cls):
        cls.target_sum = random.randint(67, 1013)

    @classmethod
    def create_numb_of_components(cls):
        cls.numb_of_components = random.randint(13, 113)

    @classmethod
    def create_upper_bound(cls):
        cls.upper_bound = random.randint(17, 1023)