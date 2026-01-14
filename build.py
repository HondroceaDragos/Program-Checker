import argparse
import subprocess
import sys

from pathlib import Path


class Interpreter:
    @classmethod
    def parse_args(cls):
        parser = argparse.ArgumentParser(description="Setup script helper")
        parser.add_argument(
            "--local", action="store_true", help="Setup the local checker env."
        )
        parser.add_argument(
            "--docker", action="store_true", help="Build the docker image"
        )

        return parser.parse_args()


class Setup:
    args = Interpreter.parse_args()

    @classmethod
    def run_script(cls, path_to_script: str = None):
        path = Path(__file__).resolve().parent / path_to_script.lstrip("/")
        try:
            subprocess.run([sys.executable, str(path)], cwd=Path(__file__).resolve().parent, check=True)
        except subprocess.CalledProcessError:
            sys.exit(1)


def main() -> None:
    if not Setup.args.local and not Setup.args.docker:
        Setup.run_script("checker/utils/setup/setup_local.py")
        Setup.run_script("checker/utils/setup/build_docker.py")
        return

    if Setup.args.local:
        Setup.run_script("checker/utils/setup/setup_local.py")
    if Setup.args.docker:
        Setup.run_script("checker/utils/setup/build_docker.py")


if __name__ == "__main__":
    main()
