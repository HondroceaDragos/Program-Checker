from rich.align import Align
from rich.panel import Panel
from rich.console import Group

class Printer:
    def __init__(self, checker):
        self.checker = checker

    def show_results(self, test_numb: int = None, program_name: str = None) -> None:
        self.checker.console.print()
        self.checker.console.print(
            Align.center(
                Panel.fit(
                    Align.center(
                        f"Now checking:   [bold yellow]{program_name}[/bold yellow]"
                    ),
                    border_style="bold yellow",
                    width=60,
                    padding=(0,2)
                )
            )
        )
        self.checker.console.print()

        stats = self.checker.compute_score(test_numb, program_name)

        tolerance = 0.003
        result_color = ""

        bad_score = self.checker.get_test_threshold("BAD")
        passable_score = self.checker.get_test_threshold("PASSABLE")

        completion = stats["completion"]
        if completion - bad_score < tolerance:
            result_color = "red"
        elif (
            tolerance <= completion - bad_score
            and completion - passable_score < tolerance
        ):
            result_color = "yellow"
        elif tolerance <= completion - passable_score:
            result_color = "green"

        tests_passed = stats["tests_passed"]
        final_score = stats["final_score"]
        max_score = stats["max_score"]
        tests = len(self.checker.get_active_tests("./input"))

        self.checker.console.print()
        summary = Group(
            Align.center(
                f"Completion: [bold {result_color}]{100 * completion:4.1f}% [/bold {result_color}]"
            ),
            Align.center(
                f"Tests passed: [bold {result_color}]{tests_passed}[/bold {result_color}] [bold white]/ {tests}[/bold white]"
            ),
            Align.center(
                f"Total score: [bold {result_color}]{final_score:4d}p[/bold {result_color}] [bold white]/ {max_score}p[/bold white]"
            ),
        )

        self.checker.console.print(
            Align.center(Panel.fit(summary, border_style=f"bold {result_color}"))
        )
        self.checker.console.print()