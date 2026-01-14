"""
Program Checker

This program is designed to grade a specific program based on a series
of input tests. The checker creates the output folder, checks it's contents to
the reference, grades and enforces time limits on the submitted code.
"""

import subprocess
import sys

from pathlib import Path

from rich.console import Console
from rich.align import Align

from utils import guards
from utils import cli


class Checker:
    """
    'Checker' class declaration and definition. Used for checking
    program output, computing score and enforcing time limits.
    """

    eps = 0.6

    input_suffix = ".txt"
    output_suffix = ".txt"
    ref_suffix = ".txt"

    console = Console(soft_wrap=True)

    TEST_SCORES = {}

    TEST_THRESHOLDS = {
        "BAD": 0.34,
        "PASSABLE": 0.75,
    }

    @classmethod
    def _call(
        cls, input_file: str = None, output_file: str = None, program_name: str = None
    ) -> tuple:
        """
        Execute one test from the input folder inside a Docker container.
        The checking is done via redirecting input and output to the container.

        Args:

            input_file (str): Path to the input file.
            output_file (str): Path to the desire output location.
            program_name (str): The name of the executable.

        Returns:

            tuple:
                -bool: Execution finished (either succesfully or interrupted by time limit).
                -float: Elapsed execution time.
        """
        try:
            output_dir_path = (
                Path(output_file).parent
                / f"{Path(program_name).stem}_output"
                / Path(output_file).name
            )
            output_dir_path.parent.mkdir(parents=True, exist_ok=True)
            with open(input_file, "r") as input, open(output_dir_path, "w") as output:
                program = subprocess.run(
                    [
                        "docker",
                        "run",
                        "--rm",
                        "-i",
                        "--init",
                        "--network",
                        "none",
                        "--memory",
                        "256m",
                        "--cpus",
                        "2",
                        "checker",
                        program_name,
                    ],
                    stdin=input,
                    stdout=output,
                    stderr=subprocess.PIPE,
                    timeout=cls.eps,
                    check=False,
                )

            time_location = program.stderr.decode()

            elapsed = None
            for line in time_location.split("\n"):
                if line.startswith("elapsed"):
                    elapsed = float(line.split("elapsed:")[1].strip())
            return (True, elapsed)

        except subprocess.TimeoutExpired:
            return (False, cls.eps)

    @classmethod
    def get_active_tests(cls, input: str = None) -> list:
        """
        Get a list of tests, based on file suffix.

        Args:
            input (str): Where the files are located.

        Returns:
            list: List of test file stems.
        """
        return [f.stem for f in Path(input).glob(f"*{cls.input_suffix}")]

    @classmethod
    def get_test_score(cls, test_name: str = None) -> int:
        """
        Get the score of a specific test.

        Args:
            test_name (str): The name of the test.

        Returns:
            int: Score of the test (or 0, if not found).
        """
        return cls.TEST_SCORES.get(test_name, 0)

    @classmethod
    def get_test_threshold(cls, tag: str = None) -> float:
        """
        Get the threshold for a specific grade.

        Args:
            tag (str): The name of the grade.

        Returns:
            float: Threshold for that grade.
        """
        return cls.TEST_THRESHOLDS.get(tag, 0)

    @classmethod
    def check_file_contents(cls, input: str = None, output: str = None) -> bool:
        """
        Check if two files are identical, byte-wise.

        Args:
            input (str): Compared file.
            output (str): File to be compared to.

        Returns:
            bool: True if contents are the same, False otherwise.
        """
        return Path(input).read_bytes().strip() == Path(output).read_bytes().strip()

    @classmethod
    def run(cls, test_numb: int = None, program_name: str = None) -> tuple:
        """
        Run multiple tests and display the outcome.

        Args:
            test_numb (int): Check only a specific test.
            program_name (str): Check the specified program.

        Returns:
            tuple:
                -int: Total score obtained.
                -int: Number of tests passed.
        """
        run_score = 0
        run_tests_passed = 0

        input_folder = Path("./input")
        test_files = list(input_folder.glob(f"*{cls.input_suffix}"))
        test_files.sort()

        if test_numb is not None:
            test_files = [test_files[test_numb - 1]]

        for test_file in test_files:
            test_name = test_file.stem
            possible_score = cls.get_test_score(test_name)

            (passed_time_check, elapsed_time) = cls._call(
                str(test_file),
                f"./output/{test_name}_out{cls.output_suffix}",
                program_name,
            )
            if passed_time_check and elapsed_time <= cls.eps:
                output_file_path = (
                    Path("./output")
                    / f"{Path(program_name).stem}_output"
                    / f"{test_name}_out{cls.output_suffix}"
                )
                if cls.check_file_contents(
                    output_file_path, f"./ref/{test_name}_ref{cls.ref_suffix}"
                ):
                    status = f'[bold green][PASSED - Elapsed time: {elapsed_time:.5f}]{" " * 11}({possible_score:2d}p / {possible_score:2d}p) [/bold green]'
                    run_score += possible_score
                    run_tests_passed += 1
                else:
                    status = f'[bold red][FAILED - Wrong result] {" " * 8}{" " * 11}( 0p / {possible_score:2d}p) [/bold red]'
            else:
                status = f'[bold red][FAILED - Time limit excedeed: {elapsed_time:.5f}]{" " * 4}( 0p / {possible_score:2d}p) [/bold red]'

            pts_numb = int(cls.console.width / 5) - len(test_name)
            cls.console.print(
                Align.center(f"[white]{test_name}{'.' * pts_numb}[/white]{status}")
            )

        return (run_score, run_tests_passed)

    @classmethod
    def build_image(cls) -> None:
        """
        Build the docker image reuired by tests.

        Exit the program if image building fails.
        """
        try:
            subprocess.run(
                [
                    sys.executable,
                    "checker/utils/setup/build_docker.py",
                ],
                cwd=Path(__file__).resolve().parent.parent,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
        except subprocess.CalledProcessError:
            sys.exit(1)

    @classmethod
    def compute_score(cls, test_numb: int = None, program_name: str = None) -> dict:
        """
        Compute the final score, completion percentage and number
        of tests passsed.

        Args:
            test_numb (int): If one test was checked, only use its score as a reference.
            program_name (str): The name of the program being checked.

        Returns:
            dict: Summary of the stats and overall score.
        """
        active_tests = sorted(cls.get_active_tests("./input"))
        if test_numb:
            active_test = active_tests[test_numb - 1]
            max_score = cls.get_test_score(active_test)
            numb_of_tests = 1
        else:
            max_score = sum(cls.get_test_score(test) for test in active_tests)
            numb_of_tests = len(active_tests)

        final_score, tests_passed = cls.run(test_numb, program_name)

        completion = 0
        if max_score == 0:
            completion = tests_passed / numb_of_tests
        else:
            completion = final_score / max_score

        return {
            "completion": completion,
            "tests_passed": tests_passed,
            "final_score": final_score,
            "max_score": max_score,
        }


@guards.swift_exit(Checker.console)
@guards.restore_cursor(Checker.console)
def main() -> None:
    """
    Program entry point

    Interpret checker flags and run tests.
    Display the final score to the user.
    """
    h = cli.Handler(Checker)
    h.handle_timeout_duration()
    h.handle_file_suffixes()

    Checker.build_image()

    h.handle_clear_terminal()
    h.handle_program_checking()


if __name__ == "__main__":
    main()
