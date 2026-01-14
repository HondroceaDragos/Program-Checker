from pathlib import Path
import subprocess
import sys


class ScriptChecker:
    timeout = 60

    @staticmethod
    def _get_scripts() -> list[Path]:
        return Path("./src").glob("*.py")

    @classmethod
    def check_scripts(cls) -> None:
        scripts = ScriptChecker._get_scripts()
        for script in scripts:
            try:
                subprocess.run(
                    [sys.executable, "./checker.py", "--name", script.name],
                    cwd=Path("./checker"),
                    timeout=cls.timeout,
                )
            except subprocess.TimeoutExpired:
                sys.exit(1)


def main() -> None:
    ScriptChecker.check_scripts()


if __name__ == "__main__":
    main()
