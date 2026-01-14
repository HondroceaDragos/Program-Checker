import argparse

class Interpreter:
    @classmethod
    def parse_args(cls):
        parser = argparse.ArgumentParser(description="Program checker v0.0.1")
        parser.add_argument("--test", type=int, help="Run a specific test")
        parser.add_argument("--name", required=True, type=str, help="Check 'name'.py")
        parser.add_argument("--eps", type=float, help="Set checker timer")
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear terminal before running the checker",
        )
        parser.add_argument("--suffixes", nargs=3, metavar=("IN", "OUT", "REF"), help="Specify file suffixes")

        return parser.parse_args()