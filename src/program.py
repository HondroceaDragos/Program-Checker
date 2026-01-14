import time
import random


def s(maximum: int) -> int:
    if maximum < 0:
        raise ValueError("Error")

    return sum(range(1, maximum + 1))


def main() -> None:
    n = int(input())

    decider = random.randint(1, 2)
    if decider % 2 == 0:
        time.sleep(1)
    try:
        print(s(n))
    except ValueError:
        print("Error")


if __name__ == "__main__":
    main()
