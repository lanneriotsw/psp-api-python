from os import geteuid
from time import sleep


def is_root() -> bool:
    """Check if is root user."""
    return geteuid() == 0


def show_delay(secs: int) -> None:
    """Flush delay time (seconds) to stdout."""
    index = int(secs)
    while index > 0:
        print(f"{index}. ", end="", flush=True)
        index -= 1
        sleep(1.0)
    print(f"{index}.")
