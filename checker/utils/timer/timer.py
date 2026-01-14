from pathlib import Path
import sys

import time
import subprocess


class ScriptResolver:
    timeout = 500

    def __init__(self, dir_path="/app"):
        self.script_path = self._get_script_path(dir_path)
        self.input_data = self._get_input_data()

    def _get_script_path(self, dir_path: str = None) -> Path:
        return Path(dir_path) / sys.argv[1]

    def _get_input_data(self) -> bytes:
        return sys.stdin.buffer.read()


def main() -> None:
    sr = ScriptResolver()

    before_call = time.perf_counter()

    try:
        subprocess.run(
            [sys.executable, str(sr.script_path)],
            input=sr.input_data,
            timeout=sr.timeout,
        )
        elapsed = time.perf_counter() - before_call
        print(f"elapsed:{elapsed:.5f}", file=sys.stderr)

    except subprocess.TimeoutExpired:
        sys.exit(1)


if __name__ == "__main__":
    main()
