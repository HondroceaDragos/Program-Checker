from generators.small_test_generator import SmallTestGenerator
from generators.medium_test_generator import MediumTestGenerator
from generators.large_test_generator import LargeTestGenerator

from pathlib import Path
from collections import defaultdict

class CustomTestFactory:
    input_dir = Path("./checker/input")
    input_dir.mkdir(exist_ok=True)

    ref_dir = Path("./checker/ref")
    ref_dir.mkdir(exist_ok=True)

    valid_test_counter = 1
    invalid_test_counter = 1

    @classmethod
    def _create_valid_test_type(cls, size:str=None, type:str=None) -> dict:
        input = []
        solution = []
        target = 0

        match size:
            case "small":
                SmallTestGenerator.create_target_sum()
                SmallTestGenerator.create_numb_of_components()
                SmallTestGenerator.create_upper_bound()

                if type == "simple":
                    input, solution = SmallTestGenerator.create_simple_true_test()
                elif type == "complex":
                    input, solution = SmallTestGenerator.create_complex_true_test()

                target = SmallTestGenerator.target_sum

                return {
                    "input": input,
                    "solution": solution,
                    "target": target
                }
            case "medium":
                MediumTestGenerator.create_target_sum()
                MediumTestGenerator.create_numb_of_components()
                MediumTestGenerator.create_upper_bound()

                if type == "simple":
                    input, solution = MediumTestGenerator.create_simple_true_test()
                elif type == "complex":
                    input, solution = MediumTestGenerator.create_complex_true_test()

                target = MediumTestGenerator.target_sum

                return {
                    "input": input,
                    "solution": solution,
                    "target": target
                }
            case "large":
                LargeTestGenerator.create_target_sum()
                LargeTestGenerator.create_numb_of_components()
                LargeTestGenerator.create_upper_bound()

                if type == "simple":
                    input, solution = LargeTestGenerator.create_simple_true_test()
                elif type == "complex":
                    input, solution = LargeTestGenerator.create_complex_true_test()

                target = LargeTestGenerator.target_sum

                return {
                    "input": input,
                    "solution": solution,
                    "target": target
                }

    @classmethod
    def build_valid_tests(cls, size:str=None, type: str=None, count: int = 1) -> None:
        for _ in range(1, count + 1):
            input_file_path = cls.input_dir / f"Valid_{size}_{type}_{cls.valid_test_counter}.txt"
            ref_file_path = cls.ref_dir / f"Valid_{size}_{type}_{cls.valid_test_counter}_ref.txt"

            cls.valid_test_counter += 1

            result = CustomTestFactory._create_valid_test_type(size, type)
            input = result["input"]
            solution = result["solution"]
            target = result["target"]

            input_lines = []
            input_lines.append(f"{len(input)} {target}")
            for number in input:
                input_lines.append(str(number))
            input_file_path.write_text("\n".join(input_lines) + "\n")


            positions = defaultdict(list)
            for idx, value in enumerate(input):
                positions[value].append(idx)
            indices = []
            for number in solution[0]:
                indices.append(positions[number].pop())
            ref_file_path.write_text(f"{len(indices)}\n{' '.join(map(str, indices))}\n{solution[0]}")

    @classmethod
    def _create_invalid_test(cls, size:str=None) -> dict:
        input = []
        solution = []
        target = 0

        match size:
                case "small":
                    SmallTestGenerator.create_target_sum()
                    SmallTestGenerator.create_numb_of_components()
                    SmallTestGenerator.create_upper_bound()

                    input, solution = SmallTestGenerator.create_false_test()

                    target = SmallTestGenerator.target_sum

                    return {
                        "input": input,
                        "solution": solution,
                        "target": target
                    }
                case "medium":
                    MediumTestGenerator.create_target_sum()
                    MediumTestGenerator.create_numb_of_components()
                    MediumTestGenerator.create_upper_bound()

                    input, solution = MediumTestGenerator.create_false_test()

                    target = MediumTestGenerator.target_sum

                    return {
                        "input": input,
                        "solution": solution,
                        "target": target
                    }
                case "large":
                    LargeTestGenerator.create_target_sum()
                    LargeTestGenerator.create_numb_of_components()
                    LargeTestGenerator.create_upper_bound()

                    input, solution = LargeTestGenerator.create_false_test()

                    target = LargeTestGenerator.target_sum

                    return {
                        "input": input,
                        "solution": solution,
                        "target": target
                    }

    @classmethod
    def build_invalid_tests(cls, size:str=None, count: int = 1) -> None:
        for _ in range(1, count + 1):
            input_file_path = cls.input_dir / f"Invalid_{size}_{cls.invalid_test_counter}.txt"
            ref_file_path = cls.ref_dir / f"Invalid_{size}_{cls.invalid_test_counter}_ref.txt"

            cls.invalid_test_counter += 1

            result = CustomTestFactory._create_invalid_test(size)
            input = result["input"]
            solution = result["solution"]
            target = result["target"]

            input_lines = []
            input_lines.append(f"{len(input)} {target}")
            for number in input:
                input_lines.append(str(number))
            input_file_path.write_text("\n".join(input_lines) + "\n")
            ref_file_path.write_text(f"0\n")


def main() -> None:
    CustomTestFactory.build_valid_tests("small", "simple", 2)
    CustomTestFactory.build_valid_tests("medium", "complex", 3)
    CustomTestFactory.build_invalid_tests("large", 2)

if __name__ == "__main__":
    main()