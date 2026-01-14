import subprocess
import sys

from process_builder import ProcessBuilder


def main() -> None:
    try:
        subprocess.run(
            ProcessBuilder.build("local"),
            check=True,
        )
    except subprocess.CalledProcessError:
        sys.exit(1)


if __name__ == "__main__":
    main()
