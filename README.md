# Program-Checker

A small, Docker-sandboxed checker for Python programs. It feeds each test input to your script over `stdin`, compares what comes back on `stdout` against a reference file, enforces a time limit, and prints a colour-coded score report in the terminal.

---

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Writing Tests](#writing-tests)
- [Command-Line Options](#command-line-options)
- [Scoring and Grading](#scoring-and-grading)
- [Sandbox and Limits](#sandbox-and-limits)
- [Configuration Reference](#configuration-reference)

---

## Features

- **Sandboxed execution**: every test runs in a throwaway Docker container with no network access, 256 MB of memory and 2 CPUs.
- **Input/reference testing**: tests are plain text files, no test framework required.
- **Time limits**: each test is timed inside the container and rejected if it exceeds the limit (0.6 s by default, configurable).
- **Readable reports**: per-test status lines, elapsed time, score, and an overall completion percentage coloured by grade (built with [`rich`](https://github.com/Textualize/rich)).
- **Batch mode**: check every script in `src/` with one command.
- **Custom per-script dependencies**: list them in `src/requirements.txt` and they are installed into the image.

## How It Works

```
checker.py --name solution.py
   │
   ├─ builds the Docker image  (docker build -t checker -f docker/Dockerfile .)
   │
   └─ for each checker/input/<test>.txt:
        docker run --rm -i --init --network none --memory 256m --cpus 2 checker solution.py
             stdin  ◄── checker/input/<test>.txt
             stdout ──► checker/output/solution_output/<test>_out.txt
             stderr ──► "elapsed:<seconds>"  (measured by the in-container timer)
        │
        └─ compare output with checker/ref/<test>_ref.txt  →  PASSED / FAILED
```

Inside the container, `timer.py` is the entrypoint. It reads the test input, runs your script with it, measures wall-clock time, and reports `elapsed:<seconds>` on `stderr` so the checker can apply the time limit.

## Project Structure

```
Program-Checker/
├── build.py                 # Setup helper (local env and/or Docker image)
├── run_all.py               # Checks every script in src/
├── src/                     # Your programs (copied into the Docker image)
│   └── requirements.txt     # Dependencies of the programs under test
├── docker/
│   └── Dockerfile           # python:3.11-slim based test image
└── checker/
    ├── checker.py           # Checker entry point
    ├── requirements.txt     # Checker dependencies (rich)
    ├── input/               # Test inputs   (<name>.txt)
    ├── ref/                 # Reference outputs (<name>_ref.txt)
    ├── output/              # Generated outputs (created at runtime)
    └── utils/
        ├── cli/             # Argument parsing and handling
        ├── guards/          # Clean Ctrl+C handling and cursor restoring
        ├── printer/         # Result rendering
        ├── setup/           # Local setup and Docker image build
        └── timer/           # In-container timing wrapper
```

## Requirements

- Python 3.10 or newer (developed and tested with Python 3.13; the setup utilities use `match` statements)
- [Docker](https://docs.docker.com/get-docker/), installed and running
- [`rich`](https://pypi.org/project/rich/) (installed by the setup step)

## Setup

```bash
git clone https://github.com/HondroceaDragos/Program-Checker.git
cd Program-Checker
python build.py
```

With no flags, `build.py` does both setup steps. You can also run them individually:

| Command | What it does |
|---------|--------------|
| `python build.py --local` | Installs the checker's Python dependencies (`checker/requirements.txt`) |
| `python build.py --docker` | Builds the `checker` Docker image from `docker/Dockerfile` |

> The checker rebuilds the Docker image at the start of every run, so changes to `src/` are always picked up.

## Usage

### Check every script in `src/`

```bash
python run_all.py
```

Each `src/*.py` file is checked in turn. If a check takes longer than 60 seconds, `run_all.py` exits with status `1`.

### Check a single script

Run the checker from the `checker/` directory and pass the script's file name (relative to `src/`):

```bash
cd checker
python checker.py --name solution.py
```

### Example

```
╭──────────────────────────────────────────────────────────╮
│                Now checking:   solution.py               │
╰──────────────────────────────────────────────────────────╯

 test1....[PASSED - Elapsed time: 0.04213]         ( 0p /  0p)
 test2....[FAILED - Wrong result]                  ( 0p /  0p)

                     Completion: 50.0%
                     Tests passed: 1 / 2
```

## Writing Tests

A test is a pair of files that share a name:

| File | Purpose |
|------|---------|
| `checker/input/<name>.txt` | Fed to the program on `stdin` |
| `checker/ref/<name>_ref.txt` | The expected `stdout` |

Example for a test called `sum_basic`:

```
checker/input/sum_basic.txt      →  2 3
checker/ref/sum_basic_ref.txt    →  5
```

Notes:

- Outputs are compared byte-for-byte after stripping leading and trailing whitespace.
- Tests run in alphabetical order. `--test N` refers to the N-th test in that order, starting from 1.
- The repository ships with a `test` pair (`test.txt` / `test_ref.txt`) containing a short sentence, which is handy for checking that the setup works.
- File suffixes are `.txt` by default and can be changed with `--suffixes`.

## Command-Line Options

`checker.py` accepts the following options (`--name` is required):

| Option | Description |
|--------|-------------|
| `--name NAME` | Script to check, e.g. `solution.py` |
| `--test N` | Run only the N-th test |
| `--eps SECONDS` | Time limit per test (default `0.6`) |
| `--clear` | Clear the terminal before printing results |
| `--suffixes IN OUT REF` | Custom file suffixes for input, output and reference files |

Examples:

```bash
python checker.py --name solution.py --test 3
python checker.py --name solution.py --eps 2.0 --clear
python checker.py --name solution.py --suffixes .in .out .ref
```

## Scoring and Grading

Each test can be worth a number of points through the `TEST_SCORES` dictionary in `checker/checker.py`:

```python
TEST_SCORES = {
    "sum_basic": 10,
    "sum_large": 20,
}
```

- Tests without an entry are worth `0` points. In that case the completion percentage is simply *tests passed / total tests*.
- Otherwise completion is *points earned / points available*.

The completion percentage determines the colour of the final summary:

| Completion | Colour | Grade |
|------------|--------|-------|
| up to 34% | red | `BAD` |
| up to 75% | yellow | `PASSABLE` |
| above 75% | green | good |

The thresholds are defined in `TEST_THRESHOLDS` in `checker/checker.py`.

## Sandbox and Limits

Every test runs with:

| Restriction | Value |
|-------------|-------|
| Network | disabled (`--network none`) |
| Memory | 256 MB |
| CPUs | 2 |
| Container lifetime | removed after each test (`--rm`) |
| Time limit | `0.6 s` by default (checker side), with a hard cap of `500 s` inside the container |

The container image is based on `python:3.11-slim`. Add any third-party packages your programs need to `src/requirements.txt`.

## Configuration Reference

| Setting | Where | Default |
|---------|-------|---------|
| Time limit per test | `Checker.eps` / `--eps` | `0.6` s |
| File suffixes | `Checker.input_suffix`, `output_suffix`, `ref_suffix` / `--suffixes` | `.txt` |
| Test scores | `Checker.TEST_SCORES` | empty |
| Grade thresholds | `Checker.TEST_THRESHOLDS` | `BAD` 0.34, `PASSABLE` 0.75 |
| Container memory / CPUs | `Checker._call` | 256 MB / 2 |
| Batch timeout | `ScriptChecker.timeout` in `run_all.py` | 60 s |
| In-container hard timeout | `ScriptResolver.timeout` in `checker/utils/timer/timer.py` | 500 s |
| Python base image | `docker/Dockerfile` | `python:3.11-slim` |
