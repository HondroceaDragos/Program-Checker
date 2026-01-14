from .interpreter import Interpreter
from ..printer import Printer

import os
import sys

class Handler:
    args = Interpreter.parse_args()

    def __init__(self, checker):
        self.checker = checker
        self.printer = Printer(checker)

    def handle_timeout_duration(self) -> None:
        if self.args.eps:
            self.checker.eps = self.args.eps

    def handle_clear_terminal(self) -> None:
        if self.args.clear:
            os.system("cls" if os.name == "nt" else "clear")

    def handle_file_suffixes(self) -> None:
        if self.args.suffixes:
            self.checker.input_suffix, self.checker.output_suffix, self.checker.ref_suffix = self.args.suffixes

    def handle_program_checking(self) -> None:
        if self.args.test is not None:
            if self.args.test <= 0 or self.args.test > len(self.checker.get_active_tests("./input")):
                self.checker.console.print(
                    "[bold red]ERROR:[/bold red] [white]Invalid test number[/white]"
                )
                sys.exit(1)
            self.printer.show_results(self.args.test, self.args.name)
        else:
            self.printer.show_results(program_name=self.args.name)