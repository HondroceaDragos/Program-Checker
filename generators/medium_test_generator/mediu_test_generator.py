from ..abs_generator._abs_generator import Generator

import random

class MediumTestGenerator(Generator):
    @classmethod
    def create_target_sum(cls):
        cls.target_sum = random.randint(1, 500)

    @classmethod
    def create_numb_of_components(cls):
        cls.numb_of_components = random.randint(5, 17)

    @classmethod
    def create_upper_bound(cls):
        cls.upper_bound = random.randint(7, 29)