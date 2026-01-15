from abc import ABC, abstractmethod

import random

class Generator(ABC):
    target_sum: int = 0
    numb_of_components: int = 1
    upper_bound: int = 1

    @classmethod
    @abstractmethod
    def create_target_sum(cls) -> None:
        pass

    @classmethod
    @abstractmethod
    def create_numb_of_components(cls) -> None:
        pass

    @classmethod
    @abstractmethod
    def create_upper_bound(cls) -> None:
        pass

    @classmethod
    def _prime_factor_decomp(cls) -> dict[int, int]:
        target = cls.target_sum

        if target == 1:
            return {1:1}

        prime_factors = {}

        for d in range(2, target + 1):
            if d * d > target:
                break

            while target % d == 0:
                prime_factors[d] = prime_factors.get(d, 0) + 1
                target //= d
        
        if target > 1:
            prime_factors[target] = prime_factors.get(target, 0) + 1
        
        return prime_factors
    
    @classmethod
    def get_valid_solution(cls) -> list[int]:
        target = cls.target_sum
        
        valid_solution = []
        bias = sum(cls._prime_factor_decomp().keys())

        while target > 1:
            if len(valid_solution) >= cls.numb_of_components - 1:
                break

            partial_complement = random.randint(1, min(target - 1, bias))
            valid_solution.append(partial_complement)
            target -= partial_complement

        valid_solution.append(target)
        
        return valid_solution
    
    @classmethod
    def create_simple_true_test(cls) -> tuple:
        sol = cls.get_valid_solution()
        input = sol.copy()

        for _ in range(1, cls.upper_bound):
            input.append(random.randint(1, cls.target_sum - 1))

        random.shuffle(input)
        return input, [sol]
    
    @classmethod
    def create_false_test(cls) -> tuple:
        sol = []
        input = []

        for _ in range(1, cls.upper_bound):
            input.append(random.randint(1, cls.target_sum - 1))

        return input, sol
    
    @classmethod
    def create_complex_true_test(cls) -> tuple[list[int], list[int]]:
        sols = [cls.get_valid_solution()]
        input = []

        for _ in range(random.randint(0, 3)):
            sols.append(cls.get_valid_solution())

        for sol in sols:
            input.extend(sol)
        
        for _ in range(1, cls.upper_bound):
            input.append(random.randint(1, cls.target_sum - 1))

        random.shuffle(input)
        return input, sols

