from os import geteuid
from time import sleep


def is_root() -> bool:
    """Check if is root user."""
    return geteuid() == 0


def show_delay(seconds: int) -> None:
    """Flush delay time to stdout."""
    while seconds > 0:
        print(f"{int(seconds)}. ", end="", flush=True)
        seconds -= 1
        sleep(1.0)
    print(f"{seconds}.")
