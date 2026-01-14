from pathlib import Path
import sys


class ProcessBuilder:
    @staticmethod
    def build(type: str = None) -> list:
        cmd = None
        match type:
            case "local":
                cmd = [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "-r",
                    "checker/requirements.txt",
                ]
            case "docker":
                cmd = [
                    "docker",
                    "build",
                    "-t",
                    "checker",
                    "-f",
                    "docker/Dockerfile",
                    ".",
                ]
            case _:
                sys.exit(1)
        return cmd
